# 供应商接入说明

## 环境

| 环境 | 基址 | 说明 |
| --- | --- | --- |
| 联调 | `https://open-sandbox.17usoft.com/supply/v2` | 数据每日重置 |
| 生产 | `https://open.17usoft.com/supply/v2` | 需白名单 |

## 鉴权

请求头携带 `X-App-Key` 与 `X-Sign`。签名规则：

1. 取所有非空参数，按参数名 ASCII 升序拼接为 `k1=v1&k2=v2`；
2. 末尾追加 `&secret=<app_secret>`；
3. 对整个字符串做 SHA-256，取小写十六进制。

`X-Timestamp` 与服务器时间偏差超过 300 秒直接拒绝。

## 接口

### 拉取订单

`GET /orders?date=YYYY-MM-DD&page=1&size=200`

响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `order_no` | string | 平台订单号 |
| `sku_code` | string | 供应商货号 |
| `qty` | int | 数量 |
| `ship_to.name` | string | 收件人 |
| `ship_to.mobile` | string | 手机号，中间四位掩码 |
| `ship_to.addr` | string | 收货地址 |

### 发货回传

`POST /orders/{order_no}/shipment`

请求体需带 `carrier`、`tracking_no`、`shipped_at`（ISO8601）。同一订单重复回传
以最后一次为准。

### 取消订阅

`DELETE /orders/{order_no}/subscription`

## 错误码

| 码 | 含义 | 处理 |
| --- | --- | --- |
| 40001 | 验签失败 | 检查参数排序与编码 |
| 40003 | 时间戳偏移 | 校准时钟 |
| 42901 | 超频 | 退避重试，最小间隔 1 秒 |
| 50002 | 下游超时 | 幂等重试 2 次 |

## 联调记录

2026-10-27 与供应商「杭州云仓」完成联调，订单拉取与发货回传均通过，遗留
`42901` 在批量回传场景下触发较频繁，建议按 50 条一批提交。
