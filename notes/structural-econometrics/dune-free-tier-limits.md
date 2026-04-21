# Dune Analytics Community/Free Tier Limits

## Monthly Credit Allocation
The **Free tier includes 2,500 credits per month** at no cost. Additional credits available at $5.00 per 100 credits.

## Query Execution Cost
Exact per-query credit costs vary based on **query complexity, data volume scanned, and processing time** rather than flat rates. The Large engine typically uses ~20 credits per execution, while smaller queries cost less.

## Row & Complexity Limits
- **Max result size**: 32GB (results truncated if exceeded)
- **No hard row cap**: Rows returned depend on query complexity and timeout constraints
- **Query timeout**: Free tier = 2-minute timeout; paid tiers support longer execution (up to 30 minutes)

## Rate Limits
- **API**: 40 requests/minute
- **Web app**: 15 requests/minute (normal), 40 requests/minute (high), combined 55/minute
- **Concurrent queries**: Limited to 3 simultaneous queries

## Key Constraint for Research
With 2,500 monthly credits and variable per-query costs (~5-20 credits typical), expect **125-500 medium-complexity queries monthly**. Budget credits carefully for iterative econometric analysis; test queries on small datasets first.

---
*Source: [Dune Docs - Credit System](https://docs.dune.com/learning/how-tos/credit-system), [Rate Limits](https://docs.dune.com/api-reference/overview/rate-limits), [Pricing FAQs](https://docs.dune.com/learning/how-tos/pricing-faqs)*
