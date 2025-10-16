# مدير موَقَّر فليكس (Mouqarr Flex Manager)

منصة متكاملة لإدارة السكان والضيوف والمدفوعات مع واجهة عربية (اتجاه من اليمين لليسار)، وخدمات خلفية تعتمد على FastAPI و SQLModel، ودعم PWA للعمل في وضع عدم الاتصال.

## المتطلبات
- Python 3.11
- Node.js 18+
- Docker (اختياري للتشغيل المتكامل)

## التشغيل المحلي

### الإعداد الخلفي
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### الإعداد الأمامي
```bash
cd frontend
npm install
npm run dev
```

## التشغيل عبر Docker
```bash
docker-compose up --build
```

## المستندات
- `docs/` يحتوي على مذكرات التصميم ودلائل الاستخدام.
- `assets/` لتخزين الشعارات والوسائط.
