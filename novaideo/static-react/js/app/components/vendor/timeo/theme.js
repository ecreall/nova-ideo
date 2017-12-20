import { lighten } from 'polished';

import getPrimaryTheme from '../../../theme';

const defaultColor = '#4580c5';

const getTheme = (primaryColor) => {
  const color = primaryColor || defaultColor;
  return {
    ...getPrimaryTheme(primaryColor),
    primary: {
      color: lighten(0.8, color),
      bgColor: color,
      appBgColor: '#fafafaff',
      lightColor: lighten(0.5, color) // for placeholder and border
    }
  };
};

export const theme = getTheme();

export default getTheme;