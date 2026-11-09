package com.ameet.fxsignals;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/** Shows the signal list (assets/index.html). Network calls are done here in Java and handed
 *  to the page, so the page never runs into browser cross-site (CORS) limits. */
public class MainActivity extends Activity {

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
    protected void onDestroy() {
        if (web != null) {
            web.destroy();
        }
        super.onDestroy();
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

    private class Bridge {

        /** GET a URL in the background; result goes to window.__httpDone(id, status, body). */
        @JavascriptInterface
        public void get(final String url, final String token, final int id) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    int status = 0;
                    String body;
                    try {
                        HttpURLConnection c = (HttpURLConnection) new URL(url).openConnection();
                        c.setConnectTimeout(15000);
                        c.setReadTimeout(20000);
                        c.setRequestProperty("Accept", "application/vnd.github.raw+json");
                        c.setRequestProperty("X-GitHub-Api-Version", "2022-11-28");
                        c.setRequestProperty("User-Agent", "FXSignals-Android");
                        c.setRequestProperty("Cache-Control", "no-cache");
                        if (token != null && token.length() > 0) {
                            c.setRequestProperty("Authorization", "Bearer " + token);
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
