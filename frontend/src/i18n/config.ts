import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
  ar: {
    translation: {
      welcome: "مرحباً بك في موَقَّر",
      dashboard: "لوحة التحكم"
    }
  },
  en: {
    translation: {
      welcome: "Welcome to Mouqarr",
      dashboard: "Dashboard"
    }
  },
  fr: {
    translation: {
      welcome: "Bienvenue à Mouqarr",
      dashboard: "Tableau de bord"
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: "ar",
  fallbackLng: ["en", "fr"],
  interpolation: { escapeValue: false }
});

export default i18n;
