package com.easydeploy.springbootquickstart.controller;

import com.alipay.api.AlipayApiException;
import com.alipay.api.AlipayClient;
import com.alipay.api.DefaultAlipayClient;
import com.alipay.api.AlipayConfig;
import com.alipay.api.domain.AlipayTradePagePayModel;
import com.alipay.api.domain.ExtUserInfo;
import com.alipay.api.domain.InvoiceKeyInfo;
import com.alipay.api.response.AlipayTradePagePayResponse;
import com.alipay.api.domain.InvoiceInfo;
import com.alipay.api.request.AlipayTradePagePayRequest;
import com.alipay.api.domain.ExtendParams;
import com.alipay.api.domain.GoodsDetail;
import com.alipay.api.domain.SubMerchant;

import java.util.ArrayList;
import java.util.List;

public class AlipayTradePagePay {

    public static void main(String[] args) throws AlipayApiException {
        // 初始化SDK
        AlipayClient alipayClient = new DefaultAlipayClient(getAlipayConfig());

        // 构造请求参数以调用接口
        AlipayTradePagePayRequest request = new AlipayTradePagePayRequest();

        // 设置业务参数到biz_content
        String bizContent = "{" +
                "\"out_trade_no\":\"daniel82AAAA000032333361X88\"," +
                "\"total_amount\":\"0.02\"," +
                "\"subject\":\"测试商品\"," +
                "\"product_code\":\"FAST_INSTANT_TRADE_PAY\"" +
                "}";

        request.setBizContent(bizContent);

        AlipayTradePagePayResponse response = alipayClient.pageExecute(request, "POST");
        String pageRedirectionData = response.getBody();
        System.out.println(pageRedirectionData);


        if (response.isSuccess()) {
            System.out.println("调用成功");
            System.out.println(response.getBody());
        } else {
            System.out.println("调用失败");
            System.out.println(response.getBody());
            // sdk版本是"4.38.0.ALL"及以上,可以参考下面的示例获取诊断链接
            // String diagnosisUrl = DiagnosisUtils.getDiagnosisUrl(response);
            // System.out.println(diagnosisUrl);
        }
    }

    private static AlipayConfig getAlipayConfig() {
        String privateKey  = "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCP/x5+6ZbVP9QknPbjByxv9i1iX0M7GYfC9qTO+03Qgf6qfbRSS+GRMfXogxobq3KFb/dydpnCr180xRUcCAH7gH3KG8WSLT931qIYaR8EpBi9Nck67R5uKb6hv/nqfr7BYxqemBQ6IJVo0T6VDl1oWE7wvYdGm0VrvEV2qFjThDxx414Z4UTuHJrNqhYZOzOfOS8xrFQm8MyFmah4JnNfQnsBgxCjL6zyqU27Id0UdS8acs6DuK6BbzCVR6tbV6y7NVrL/byfivRx2dOw9b+dv5akFdtQNkvJ4IWdKgYMvJSmxtUEdFfEbCAZGMhadIU33cjAw1E4gWTezl8+bloRAgMBAAECggEAZBBfOsZMYKhYXZEOJ7nGcY9a/m9AowMcyqjm4kbUTj7nn8Z21nGQsHtNbWQdcnjzvjKOe+Za92Uy/dKu1qnh5snln9sosmnrHvXx8pCqU2lNH78OtXotmVQ8+t4TZ5boLC8YQnlgJPyblxlBKgevdWFYigbKyJAB79oHU2utPl4pnkDmFzjOFy+OyG7J0kY0ZKS25YIXMyTSt9HOMLOozigw4cp+ZK+5TT2Lqqiv1m1OZZjDSPUEXjxWoTOqFqdUstfSgI0kHtRf260EAnX7UqJv5Ougb6hcKm5EYPrffzL8YYuvA6niaIudX4zUu24mZqUDCj1IG074hMORLPUjuQKBgQDjFbaiKsuMRrUWR5DGMKuD2IHKlpf7f+vTUqtc6DTAikbFyAeFKnmeBPuuFjoKJCIVXyhOP+X8b+vOMQ8OxNbzg8sSKhc94WoWvnwEf8KdflEjGGiSYnU/sL3CjnnHmWtgxf7Gvd0jnJV8yQefsDdig1CAfWkejZ+hYJixso50+wKBgQCiVPoKU4fHbSu9/q/bdxpnCIjDIWASJ+P9NXf6/EEEKQlt0wjN3MGgdJq4V64DTvTZ4ZCUvSYj5s+L6YJPNHM8fh2RyM/tiVH4BM0fL0E+YfQy59VSlCXerLCATe5VN0H7m2SoqN3LTo6Y6DKXkcr+JAA0HBeYnwmhS5LVILjHYwKBgAxIi2WAPRxsYrU+z8T4sv5hwruLo9L123LF4QEYimnz0No39LguUP/MMzT6fM85nyJa0FpTOISMJUw0+SSKXzoy4dQstK8jN1LdoOW5Z3SPdaIZWua4LrFwRQN2I345fUZxz1M+x+x6NtfWI/RuWsCYa81Xe00syfq3t+q8xtnrAoGATwE8kDoHIzAm0dlajV1yJCMrLIzZzPxNIbccJbMPkY7HYAQNjOOb+RPHGWDS+Bk9Ya0+SKWmImL7MAT9vr6wNwjKK2GokNr8YdE0Y7ED9/CEgSID2KTxqWYyoL9M93xlSKdgXhWRnJknHZQky0/Rk87BqprhgQ4mCbJWTBQY2jECgYAeNZ79dUEiInxjWIM3seVv989sJbHeSsXINU+o+7yBYmkvLk7yqrnSh9WLIoo4iAvPFwZvC3EGtbsyQwiQKIGbUhQHpPQ2iDjMolXCj2LQHp1DhwgrBiKqCw69YQkZ3h2cDFL2R6YzM78WGmPxDB7+yXFzL+7I2k4xPTqJSICIjQ==";
        String alipayPublicKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAihHqYBxL0pcsp9KAQfozI2l1mrIMa6Z/ebxQd8z6itD1tZDAR4tOQs/XbyoUCknLdOfX2Ur2b3K5Z6YSGaaCI/5XJv1gw6c4e0mdtmzElqtSZRYt/6fSedvONUlfE+bRJ9cZJ1VpTp2w83zVrsHQ6JHHTY26wlg5L/KeOEweLnYeS/376WlcRWTvabRbum/JE/XbTvg98taFVdQwbz19e5xKrsqepjmO+pjljphWAq434PTMmQCgzGOwFmEjfoFwPWKz8QCYGla2h/bLquEf8iA33wSYFF8V/AD2Hc7goq5TRl4HNPh9MlYtcrqjPxzvtxZ3cC386GtF3ez58c/MHwIDAQAB";
        AlipayConfig alipayConfig = new AlipayConfig();
        alipayConfig.setServerUrl("https://openapi-sandbox.dl.alipaydev.com/gateway.do");
        alipayConfig.setAppId("9021000141697639");
        alipayConfig.setPrivateKey(privateKey);
        alipayConfig.setFormat("json");
        alipayConfig.setAlipayPublicKey(alipayPublicKey);
        alipayConfig.setCharset("UTF-8");
        alipayConfig.setSignType("RSA2");
        return alipayConfig;
    }
}