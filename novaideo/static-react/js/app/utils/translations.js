/* eslint max-len: "off", quotes: ["error", "double"] */
const Translations = {
  fr: {
    date: {
      format: "D MMMM YYYY",
      format2: "DD-MM-YYYY",
      format3: "D MMMM YYYY h \\h mm",
      today: "Today"
    },
    time: {
      format: "h \\h mm"
    }
  },
  en: {
    date: {
      format: "MMMM Do, YYYY",
      format2: "YYYY-MM-DD",
      format3: "MMMM Do, YYYY h \\h mm",
      today: "Aujourd'hui"
    },
    time: {
      format: "h \\h mm"
    }
  }
};

module.exports = Translations; // keep commonJS syntax for the node i18n:export script to work