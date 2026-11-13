package com.ameet.fxsignals;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

/** Shows the app screens (assets/index.html). Network calls are done here in Java and handed
 *  to the page, so the page never runs into browser cross-site (CORS) limits. */
public class MainActivity extends Activity {

    private static final String BROWSER_UA =
            "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36";

    private WebView web;
    private Uri lastZipUri;          // last saved .zip, for the Share button

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.parseColor("#0F1419"));
        getWindow().setNavigationBarColor(Color.parseColor("#0F1419"));

        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#0F1419"));
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(web, true);   // TradingView chart
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (url.startsWith("file:///android_asset/")) {
                    return false;
                }
                if (request.isForMainFrame()) {          // a link inside the chart: open in the browser
                    openExternal(url);
                    return true;
                }
                return false;
            }
        });
        web.addJavascriptInterface(new Bridge(), "Android");
        setContentView(web);
        web.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) {
            web.evaluateJavascript("window.onAppResume && window.onAppResume()", null);
        }
    }

    @Override
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        if (web == null) {
            super.onBackPressed();
            return;
        }
        // Let the page close the chart screen first; if it doesn't, leave the app.
        web.evaluateJavascript("(window.onBack && window.onBack()) ? 'handled' : 'no'", new ValueCallback<String>() {
            @Override
            public void onReceiveValue(String value) {
                if (value == null || !value.contains("handled")) {
                    finish();
                }
            }
        });
    }

    @Override
    protected void onDestroy() {
        if (web != null) {
            web.destroy();
        }
        super.onDestroy();
    }

    private void openExternal(String url) {
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        } catch (Exception e) {
            Toast.makeText(this, "Can't open link", Toast.LENGTH_SHORT).show();
        }
    }

    private static byte[] readAll(InputStream in) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buf = new byte[8192];
        int n;
        while ((n = in.read(buf)) != -1) {
            out.write(buf, 0, n);
        }
        in.close();
        return out.toByteArray();
    }

    /** Plain GET. Returns {status, body}. status 0 = no connection. */
    private static Object[] fetchBytes(String url, Map<String, String> headers) {
        int status = 0;
        byte[] body;
        try {
            HttpURLConnection c = (HttpURLConnection) new URL(url).openConnection();
            c.setConnectTimeout(15000);
            c.setReadTimeout(30000);
            c.setUseCaches(false);
            for (Map.Entry<String, String> h : headers.entrySet()) {
                c.setRequestProperty(h.getKey(), h.getValue());
            }
            status = c.getResponseCode();
            InputStream in = status >= 400 ? c.getErrorStream() : c.getInputStream();
            body = in == null ? new byte[0] : readAll(in);
            c.disconnect();
        } catch (Exception e) {
            body = String.valueOf(e.getMessage()).getBytes();
        }
        return new Object[]{status, body};
    }

    private static Map<String, String> githubHeaders(String accept, String token) {
        Map<String, String> h = new HashMap<>();
        h.put("Accept", accept);
        h.put("X-GitHub-Api-Version", "2022-11-28");
        h.put("User-Agent", "FXSignals-Android");
        h.put("Cache-Control", "no-cache");
        if (token != null && token.length() > 0) {
            h.put("Authorization", "Bearer " + token);
        }
        return h;
    }

    private static Map<String, String> webHeaders() {
        Map<String, String> h = new HashMap<>();
        h.put("Accept", "application/json,text/plain,*/*");
        h.put("User-Agent", BROWSER_UA);
        return h;
    }

    /** Sends a JS call back to the page on the UI thread. */
    private void callJs(final String js) {
        web.post(new Runnable() {
            @Override
            public void run() {
                web.evaluateJavascript(js, null);
            }
        });
    }

    /** GET a URL on a background thread; result goes to window.__httpDone(id, status, body). */
    private void httpGet(final String url, final Map<String, String> headers, final int id) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                Object[] r = fetchBytes(url, headers);
                String body;
                try {
                    body = new String((byte[]) r[1], "UTF-8");
                } catch (Exception e) {
                    body = "";
                }
                callJs("window.__httpDone(" + id + "," + r[0] + "," + JSONObject.quote(body) + ")");
            }
        }).start();
    }

    /** Saves bytes as a file in Downloads/FXSignals. Returns a path to show the user. */
    private String saveToDownloads(String name, byte[] data) throws Exception {
        if (Build.VERSION.SDK_INT >= 29) {
            ContentValues v = new ContentValues();
            v.put(MediaStore.MediaColumns.DISPLAY_NAME, name);
            v.put(MediaStore.MediaColumns.MIME_TYPE, "application/zip");
            v.put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/FXSignals");
            Uri uri = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, v);
            if (uri == null) {
                throw new Exception("could not create the file");
            }
            OutputStream os = getContentResolver().openOutputStream(uri);
            if (os == null) {
                throw new Exception("could not open the file");
            }
            os.write(data);
            os.close();
            lastZipUri = uri;
            return "Downloads/FXSignals/" + name;
        }
        // Android 8 and 9: the app's own folder (no storage permission needed)
        File dir = getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS);
        if (dir == null) {
            dir = getFilesDir();
        }
        File f = new File(dir, name);
        FileOutputStream fos = new FileOutputStream(f);
        fos.write(data);
        fos.close();
        lastZipUri = null;
        return f.getAbsolutePath();
    }

    private class Bridge {

        /** GitHub file as raw text (signals.json). */
        @JavascriptInterface
        public void get(String url, String token, int id) {
            httpGet(url, githubHeaders("application/vnd.github.raw+json", token), id);
        }

        /** GitHub API as JSON (e.g. the list of files in the repository). */
        @JavascriptInterface
        public void api(String url, String token, int id) {
            httpGet(url, githubHeaders("application/vnd.github+json", token), id);
        }

        /** Any other request, e.g. chart prices. */
        @JavascriptInterface
        public void fetch(String url, int id) {
            httpGet(url, webHeaders(), id);
        }

        /**
         * Builds a .zip and saves it to Downloads.
         * spec: JSON list of {"name": path in zip, "text": content} or {"name", "url", "github": true/false}.
         * Result goes to window.__zipDone(id, {"ok", "where", "files", "failed", "canShare", "error"}).
         */
        @JavascriptInterface
        public void saveZip(final String spec, final String zipName, final String token, final int id) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    JSONObject res = new JSONObject();
                    try {
                        JSONArray items = new JSONArray(spec);
                        ByteArrayOutputStream bos = new ByteArrayOutputStream();
                        ZipOutputStream zip = new ZipOutputStream(bos);
                        int failed = 0;
                        for (int i = 0; i < items.length(); i++) {
                            JSONObject it = items.getJSONObject(i);
                            String name = it.getString("name");
                            byte[] data;
                            if (it.has("text")) {
                                data = it.getString("text").getBytes("UTF-8");
                            } else {
                                boolean gh = it.optBoolean("github", false);
                                Map<String, String> h = gh ? githubHeaders("application/vnd.github.raw+json", token) : webHeaders();
                                Object[] r = fetchBytes(it.getString("url"), h);
                                int status = (Integer) r[0];
                                if (status == 200) {
                                    data = (byte[]) r[1];
                                } else {
                                    failed++;
                                    name = name + ".error.txt";
                                    data = ("Could not download " + it.getString("url") + " (HTTP " + status + ")").getBytes("UTF-8");
                                }
                            }
                            zip.putNextEntry(new ZipEntry(name));
                            zip.write(data);
                            zip.closeEntry();
                        }
                        zip.close();
                        String where = saveToDownloads(zipName, bos.toByteArray());
                        res.put("ok", true);
                        res.put("where", where);
                        res.put("files", items.length());
                        res.put("failed", failed);
                        res.put("canShare", lastZipUri != null);
                    } catch (Exception e) {
                        try {
                            res.put("ok", false);
                            res.put("error", String.valueOf(e.getMessage()));
                        } catch (Exception ignored) {
                            // nothing else to do
                        }
                    }
                    callJs("window.__zipDone(" + id + "," + res.toString() + ")");
                }
            }).start();
        }

        /** Opens Android's share sheet for the last saved .zip (WhatsApp, Gmail, Drive, Claude...). */
        @JavascriptInterface
        public void shareLast() {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if (lastZipUri == null) {
                        Toast.makeText(MainActivity.this, "Download the logs first", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    Intent send = new Intent(Intent.ACTION_SEND);
                    send.setType("application/zip");
                    send.putExtra(Intent.EXTRA_STREAM, lastZipUri);
                    send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    try {
                        startActivity(Intent.createChooser(send, "Share logs"));
                    } catch (Exception e) {
                        Toast.makeText(MainActivity.this, "No app to share with", Toast.LENGTH_SHORT).show();
                    }
                }
            });
        }

        @JavascriptInterface
        public void open(final String url) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    openExternal(url);
                }
            });
        }

        @JavascriptInterface
        public void copy(final String text) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                    if (cm != null) {
                        cm.setPrimaryClip(ClipData.newPlainText("price", text));
                        Toast.makeText(MainActivity.this, "Copied " + text, Toast.LENGTH_SHORT).show();
                    }
                }
            });
        }
    }
}
