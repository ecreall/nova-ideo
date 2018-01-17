import { teal, grey, deepOrange, orange, blue } from 'material-ui/colors';
import { createMuiTheme } from 'material-ui/styles';

function theme() {
  return createMuiTheme({
    palette: {
      primary: {
        ...teal
      },
      secondary: grey,
      tertiary: {
        color: blue[500],
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