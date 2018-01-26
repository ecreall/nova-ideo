import { teal, grey, deepOrange, orange, blue } from 'material-ui/colors';
import { createMuiTheme } from 'material-ui/styles';

const primaryCode = 500;

function theme() {
  return createMuiTheme({
    palette: {
      primary: {
        ...teal,
        [primaryCode]: '#4D394B', // test color to remove.
        light: '#cac4c9',
        dark: '#342032',
        dark2: '#2a1628'
      },
      secondary: grey,
      tertiary: {
        color: '#4C9689',
        hover: {
          color: 'white'
        }
      },
      danger: deepOrange,
      info: blue,
      warning: orange
    },
    typography: {
      htmlFontSize: 15,
      fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif'
    },
    body1: {
      margin: 0
    }
  });
}

export default theme;