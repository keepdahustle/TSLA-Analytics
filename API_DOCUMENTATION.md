# TSLA Analytics - API Documentation

## Base URL
```
Production: https://your-domain.vercel.app/api
Development: http://localhost:5000/api
```

## Authentication
Currently no authentication required. Consider adding for production.

## Response Format
All responses return JSON with the following structure:

### Success Response
```json
{
  "status": "success",
  "data": [...],
  "count": 100
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "code": 400
}
```

---

## Endpoints

### Health Check
Check if API is running and database is connected.

**Endpoint:**
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000",
  "service": "TSLA Analytics API"
}
```

---

### Stock Data Endpoints

#### Get All Stock Data
Retrieve all Tesla stock data from database.

**Endpoint:**
```
GET /api/stock/all
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "Date": "2010-06-29",
      "Close": 1.59,
      "High": 1.67,
      "Low": 1.17,
      "Open": 1.27,
      "Volume": 281494500,
      "Year": 2010,
      "Quarter": 2,
      "Month": 6
    }
  ],
  "count": 3922
}
```

**Query Parameters:** None

**Limits:** Returns all records (use with caution for large datasets)

---

#### Get Stock Data by Year
Retrieve stock data for a specific year.

**Endpoint:**
```
GET /api/stock/year/{year}
```

**Path Parameters:**
- `year` (required): Year as integer (e.g., 2024)

**Example:**
```
GET /api/stock/year/2024
```

**Response:**
```json
{
  "status": "success",
  "year": 2024,
  "data": [
    {
      "Date": "2024-01-02",
      "Close": 250.08,
      "High": 255.99,
      "Low": 248.45,
      "Open": 251.00,
      "Volume": 45678900
    }
  ],
  "count": 252
}
```

---

#### Get Stock Data by Year and Quarter
Retrieve stock data for specific year and quarter.

**Endpoint:**
```
GET /api/stock/year/{year}/quarter/{quarter}
```

**Path Parameters:**
- `year` (required): Year as integer (e.g., 2024)
- `quarter` (required): Quarter as integer (1-4)

**Example:**
```
GET /api/stock/year/2024/quarter/1
```

**Response:**
```json
{
  "status": "success",
  "year": 2024,
  "quarter": 1,
  "data": [...],
  "count": 63
}
```

**Note:** Quarter 1 = Jan-Mar, 2 = Apr-Jun, 3 = Jul-Sep, 4 = Oct-Dec

---

#### Get Latest Stock Prices
Retrieve latest N days of stock prices.

**Endpoint:**
```
GET /api/stock/latest
```

**Query Parameters:**
- `days` (optional): Number of days, default is 30

**Examples:**
```
GET /api/stock/latest                    # Last 30 days
GET /api/stock/latest?days=7             # Last 7 days
GET /api/stock/latest?days=90            # Last 90 days
```

**Response:**
```json
{
  "status": "success",
  "days": 30,
  "data": [
    {
      "Date": "2024-01-09",
      "Close": 238.11
    }
  ],
  "count": 30
}
```

---

### Model Evaluation Endpoints

#### Get Model Evaluation Metrics
Retrieve performance metrics for all trained models.

**Endpoint:**
```
GET /api/models/evaluation
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "Model": "SARIMA",
      "MAE": 36.7567,
      "RMSE": 39.1818,
      "MAPE (%)": 19.58,
      "R²": -2.3171,
      "Dir Accuracy": 0.5167,
      "Dir Precision": 0.4722,
      "Dir Recall": 0.6296,
      "Dir F1": 0.5397
    },
    {
      "Model": "Prophet",
      "MAE": 56.9407,
      "RMSE": 60.8691,
      "MAPE (%)": 30.55,
      "R²": -7.0055,
      "Dir Accuracy": 0.0,
      "Dir Precision": 0.0,
      "Dir Recall": 0.0,
      "Dir F1": 0.0
    }
  ],
  "count": 2
}
```

**Metrics Explanation:**
- **MAE**: Mean Absolute Error (lower is better)
- **RMSE**: Root Mean Square Error (lower is better)
- **MAPE**: Mean Absolute Percentage Error (lower is better)
- **R²**: Coefficient of Determination (higher is better, max 1.0)
- **Dir Accuracy**: Directional Accuracy (percentage correct direction)
- **Dir Precision**: Precision for directional prediction
- **Dir Recall**: Recall for directional prediction
- **Dir F1**: F1 Score for directional prediction

---

### Prediction Endpoints

#### Get SARIMA Predictions
Retrieve SARIMA model predictions.

**Endpoint:**
```
GET /api/predictions/sarima
```

**Response:**
```json
{
  "status": "success",
  "model": "SARIMA",
  "data": [
    {
      "Date": "2024-01-02",
      "Actual": 250.08,
      "SARIMA_Pred": 256.82
    }
  ],
  "count": 61
}
```

---

#### Get Prophet Predictions
Retrieve Prophet model predictions.

**Endpoint:**
```
GET /api/predictions/prophet
```

**Response:**
```json
{
  "status": "success",
  "model": "Prophet",
  "data": [
    {
      "Date": "2024-01-02",
      "Actual": 250.08,
      "Prophet_Pred": 252.70
    }
  ],
  "count": 61
}
```

---

#### Get Combined Predictions
Retrieve predictions from both models side-by-side for comparison.

**Endpoint:**
```
GET /api/predictions/combined
```

**Response:**
```json
{
  "status": "success",
  "models": ["SARIMA", "Prophet"],
  "data": [
    {
      "Date": "2024-01-02",
      "Actual": 250.08,
      "SARIMA_Pred": 256.82,
      "Prophet_Pred": 252.70
    }
  ],
  "count": 61
}
```

---

## Error Codes

| Code | Message | Explanation |
|------|---------|-------------|
| 200 | Success | Request successful |
| 400 | Bad Request | Invalid parameters (e.g., invalid quarter) |
| 404 | Not Found | Endpoint does not exist |
| 500 | Server Error | Database or application error |

### Error Examples

**Invalid Quarter:**
```json
{
  "status": "error",
  "message": "Invalid quarter (1-4)",
  "code": 400
}
```

**Invalid Endpoint:**
```json
{
  "status": "error",
  "message": "Endpoint not found",
  "code": 404
}
```

**Server Error:**
```json
{
  "status": "error",
  "message": "Internal server error",
  "code": 500
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- Implement per-IP rate limiting
- Use tools like Flask-Limiter
- Consider API key authentication

---

## CORS Configuration

API supports CORS requests. Allowed origins depend on deployment configuration.

**Headers:**
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

---

## Data Types

| Type | Description | Example |
|------|-------------|---------|
| Date | ISO 8601 format | "2024-01-15" |
| Float | Decimal number | 250.5 |
| Integer | Whole number | 2024 |
| String | Text | "SARIMA" |

---

## Integration Examples

### JavaScript/Fetch
```javascript
async function getStockData() {
  const response = await fetch('https://your-domain.vercel.app/api/stock/latest?days=30');
  const data = await response.json();
  console.log(data.data);
}
```

### Python/Requests
```python
import requests

response = requests.get('https://your-domain.vercel.app/api/stock/latest?days=30')
data = response.json()
print(data['data'])
```

### cURL
```bash
curl https://your-domain.vercel.app/api/stock/latest?days=30
```

### Axios
```javascript
import axios from 'axios';

const data = await axios.get('https://your-domain.vercel.app/api/predictions/combined');
console.log(data.data.data);
```

---

## Pagination

Currently no pagination implemented. For large datasets, consider:
- Implementing `limit` and `offset` parameters
- Adding cursor-based pagination
- Using data streaming

---

## Caching

Responses are not cached by default. For production:
- Implement Redis caching
- Set appropriate Cache-Control headers
- Cache by endpoint popularity

---

## Performance Tips

1. **Use specific endpoints** instead of `/api/stock/all`
   - ✓ Good: `GET /api/stock/year/2024`
   - ✗ Bad: `GET /api/stock/all` for just 2024 data

2. **Limit date ranges** with query parameters
   - Use `?days=30` instead of getting all predictions

3. **Cache results** on client side for frequently accessed data

4. **Batch requests** when possible to reduce API calls

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial API release
- All endpoints functional
- PostgreSQL integration complete

---

## Support

For API issues or questions:
1. Check error messages carefully
2. Review endpoint documentation above
3. Check query parameters
4. Verify database connectivity
5. Check application logs

---

## Future Enhancements

- [ ] Add authentication/API keys
- [ ] Implement pagination
- [ ] Add filtering options
- [ ] Add sorting parameters
- [ ] Implement caching
- [ ] Add rate limiting
- [ ] Support CSV export
- [ ] Add WebSocket for real-time updates
