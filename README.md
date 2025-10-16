# Mouqarr Flex Manager

منصة إدارة مقار مرنة للمقيمين والضيوف تعتمد على **FastAPI + React (Vite)** مع دعم كامل للغة العربية والاتجاه من اليمين إلى اليسار.

## المتطلبات

- Python 3.11
- Node.js 18+
- (اختياري) Docker و Docker Compose

## الإعداد السريع

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
python backend/seed.py  # بيانات تجريبية
uvicorn app.main:app --reload --app-dir backend
```

وفي نافذة أخرى:

```bash
cd frontend
npm install
npm run dev
```

- الواجهة الخلفية: [http://localhost:8000](http://localhost:8000)
- الواجهة الأمامية: [http://localhost:5173](http://localhost:5173)

## Docker Compose

```bash
docker-compose up --build
```

## الاختبارات

```bash
pytest backend/tests -q
```

## الهيكلية

```
backend/
  app/
    core/        # الإعدادات العامة
    models/      # نماذج SQLModel
    routers/     # مسارات FastAPI (مقيمون، ضيوف، حجوزات، دفعات، إعدادات، مصادقة)
    services/    # الخدمات (إشغال، PDF، تكامل Google)
    utils/       # المساعدة مثل JWT
  tests/         # اختبارات Pytest
frontend/
  src/
    layouts/     # تخطيط لوحة التحكم
    pages/       # صفحات رئيسية
    store/       # حالة المصادقة
```

## المزايا المنفذة

- CRUD للمقيمين، الضيوف، الحجوزات، الدفعات، الإعدادات.
- توليد إيصالات PDF تلقائيًا باستخدام fpdf2.
- تحذيرات تجاوز السعة للحجوزات.
- تكامل Google Sheets عبر gspread (إعداد بيانات الاعتماد + منع التكرار).
- مهام مجدولة بالتوقيتات المطلوبة عبر APScheduler.
- مصادقة JWT مع حساب إداري افتراضي (admin/admin).
- واجهة عربية RTL مع تنقل واضح وصفحات أساسية.
- Seed script لبيانات تجريبية.
- اختبارات أساسية (إشغال، استيراد Google، توليد PDF).
- Docker Compose لتشغيل الواجهة الأمامية والخلفية.
