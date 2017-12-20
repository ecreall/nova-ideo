import { lighten } from 'polished';

const defaultColor = '#54902a';

const getTheme = (primaryColor) => {
  const color = primaryColor || defaultColor;
  return {
    color: {
      gray: '#a5a2a2',
      red: 'red',
      orange: '#ef6e18',
      blue: '#4580c5'
    },
    primary: {
      color: lighten(0.8, color),
      bgColor: color,
      appBgColor: '#fafafaff',
      lightColor: lighten(0.5, color) // for placeholder and border
    },
    secondary: {
      // used for secondary buttons
      color: '#6d6d6d',
      bgColor: '#fafafaff'
    }
  };
};

export const theme = getTheme();

export default getTheme;