/* eslint max-len: "off", quotes: ["error", "double"] */
const Translations = {
  fr: {
    date: {
      format: "D MMMM YYYY",
      format2: "DD-MM-YYYY"
    }
  },
  en: {
    date: {
      format: "MMMM Do, YYYY",
      format2: "YYYY-MM-DD"
    }
  }
};

module.exports = Translations; // keep commonJS syntax for the node i18n:export script to work