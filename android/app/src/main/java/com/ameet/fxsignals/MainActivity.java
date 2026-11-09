package com.ameet.fxsignals;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

/** Shows the app screens (assets/index.html). Network calls are done here in Java and handed
 *  to the page, so the page never runs into browser cross-site (CORS) limits. */
public class MainActivity extends Activity {

    private static final String BROWSER_UA =
            "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36";

    private WebView web;

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

    private static String readAll(InputStream in) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buf = new byte[8192];
        int n;
        while ((n = in.read(buf)) != -1) {
            out.write(buf, 0, n);
        }
        in.close();
        return out.toString("UTF-8");
    }

    /** GET a URL on a background thread; result goes to window.__httpDone(id, status, body). */
    private void httpGet(final String url, final Map<String, String> headers, final int id) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                int status = 0;
                String body;
                try {
                    HttpURLConnection c = (HttpURLConnection) new URL(url).openConnection();
                    c.setConnectTimeout(15000);
                    c.setReadTimeout(20000);
                    c.setUseCaches(false);
                    for (Map.Entry<String, String> h : headers.entrySet()) {
                        c.setRequestProperty(h.getKey(), h.getValue());
                    }
                    status = c.getResponseCode();
                    InputStream in = status >= 400 ? c.getErrorStream() : c.getInputStream();
                    body = in == null ? "" : readAll(in);
                    c.disconnect();
                } catch (Exception e) {
                    body = String.valueOf(e.getMessage());
                }
                final String js = "window.__httpDone(" + id + "," + status + "," + JSONObject.quote(body) + ")";
                web.post(new Runnable() {
                    @Override
                    public void run() {
                        web.evaluateJavascript(js, null);
                    }
                });
            }
        }).start();
    }

    private class Bridge {

        /** GitHub API request (signals.json). */
        @JavascriptInterface
        public void get(String url, String token, int id) {
            Map<String, String> h = new HashMap<>();
            h.put("Accept", "application/vnd.github.raw+json");
            h.put("X-GitHub-Api-Version", "2022-11-28");
            h.put("User-Agent", "FXSignals-Android");
            h.put("Cache-Control", "no-cache");
            if (token != null && token.length() > 0) {
                h.put("Authorization", "Bearer " + token);
            }
            httpGet(url, h, id);
        }

        /** Any other request, e.g. chart prices. */
        @JavascriptInterface
        public void fetch(String url, int id) {
            Map<String, String> h = new HashMap<>();
            h.put("Accept", "application/json,text/plain,*/*");
            h.put("User-Agent", BROWSER_UA);
            httpGet(url, h, id);
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
