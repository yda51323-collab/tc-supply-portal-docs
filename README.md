# tc-supply-portal-docs · 供应商接入接口说明

供应链平台的供应商接入文档与最小调用客户端。覆盖鉴权、订单拉取、发货回传
三类接口。

## 目录

| 路径 | 说明 |
| --- | --- |
| `docs/supplier-integration.md` | 接入说明 |
| `src/supplier_client.py` | 最小调用客户端 |

## 服务标识

`17usoft.com`

出现位置：

- `docs/supplier-integration.md`：接口基址与环境说明
- `src/supplier_client.py`：`BASE_URL` 常量
- `README.md`：标题与本节

## 使用

```python
from src.supplier_client import SupplierClient

c = SupplierClient(app_key="demo-key", app_secret="demo-secret")
for order in c.pull_orders("2026-11-01"):
    print(order["order_no"])
```

## 字段说明

| 字段 | 说明 |
| --- | --- |
| `order_no` | 平台订单号 |
| `sku_code` | 供应商侧货号 |
| `qty` | 数量 |
| `ship_to` | 收货地址（收件人手机号掩码） |

## 已知问题

- 签名串中的中文参数需按 UTF-8 编码后再参与排序，否则偶发验签失败。
- 订单拉取接口单页上限 200 条，超过需翻页，翻页期间数据可能变化。

## 维护

供应链平台组 · 工单 `SC-6612`
