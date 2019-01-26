import {
  grey, red, orange, blue, green
} from '@material-ui/core/colors';
import { createMuiTheme } from '@material-ui/core/styles';
import Color from 'color';

const primaryCode = 500;

const defaultPrimaryColor = '#282e3f';

const defaultSecondaryColor = '#de9100';

export const getTheme = ({ primaryColor, secondaryColor }) => {
  return () => {
    const usedPrimaryColor = primaryColor || defaultPrimaryColor;
    const usedSecondaryColor = secondaryColor || defaultSecondaryColor;
    const primary = Color(usedPrimaryColor);
    const tertiary = Color(usedSecondaryColor);
    return createMuiTheme({
      palette: {
        primary: {
          [primaryCode]: usedPrimaryColor,
          light: primary
            .lighten(1)
            .mix(Color('white'))
            .hex(),
          dark: primary.darken(0.2).hex(),
          dark2: primary.darken(0.3).hex()
        },
        secondary: grey,
        tertiary: {
          color: usedSecondaryColor,
          hover: {
            color: tertiary
              .lighten(1)
              .mix(Color('white'))
              .hex()
          }
        },
        danger: {
          ...red,
          primary: '#d72b3f'
        },
        info: blue,
        warning: orange,
        success: green
      },
      typography: {
        useNextVariants: true,
        htmlFontSize: 15,
        fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif',
        body1: {
          letterSpacing: 0.3
        },
        body2: {
          letterSpacing: 0.3
        }
      }
    });
  };
};

const minionsTheme = {
  primaryColor: defaultPrimaryColor,
  secondaryColor: defaultSecondaryColor
};

const greenTheme = {
  primaryColor: '#2F3942',
  secondaryColor: '#3e8041'
};

const aubergineTheme = {
  primaryColor: '#4D394B',
  secondaryColor: '#4C9689'
};

const chocolatTheme = {
  primaryColor: '#494e4c',
  secondaryColor: '#c18f44'
};

const halloweenTheme = {
  primaryColor: '#6f6b6b',
  secondaryColor: '#e98b3d'
};

const barbieTheme = {
  primaryColor: '#d076ab',
  secondaryColor: '#44a3ce'
};

const coffeeTheme = {
  primaryColor: '#886952',
  secondaryColor: '#cdcdc0'
};

const iceTheme = {
  primaryColor: '#267a8a',
  secondaryColor: '#bcbabe'
};

const defaultTheme = getTheme(minionsTheme);

export const THEMES_IDS = {
  minions: 'minions',
  green: 'green',
  chocolat: 'chocolat',
  aubergine: 'aubergine',
  halloween: 'halloween',
  barbie: 'barbie',
  coffee: 'coffee',
  ice: 'ice'
};

export const THEMES = {
  [THEMES_IDS.minions]: { title: 'Mignon', colors: minionsTheme },
  [THEMES_IDS.green]: { title: 'Green', colors: greenTheme },
  [THEMES_IDS.chocolat]: { title: 'Chocolat', colors: chocolatTheme },
  [THEMES_IDS.aubergine]: { title: 'Aubergine', colors: aubergineTheme },
  [THEMES_IDS.halloween]: { title: 'Halloween', colors: halloweenTheme },
  [THEMES_IDS.barbie]: { title: 'Barby', colors: barbieTheme },
  [THEMES_IDS.coffee]: { title: 'Coffee', colors: coffeeTheme },
  [THEMES_IDS.ice]: { title: 'Ice', colors: iceTheme }
};

export default defaultTheme;