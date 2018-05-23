import { teal, grey, red, orange, blue, green } from '@material-ui/core/colors';
import { createMuiTheme } from '@material-ui/core/styles';

const primaryCode = 500;

// function theme() {
//   return createMuiTheme({
//     palette: {
//       primary: {
//         ...teal,
//         [primaryCode]: '#4D394B', // test color to remove.
//         light: '#cac4c9',
//         dark: '#342032',
//         dark2: '#2a1628'
//       },
//       secondary: grey,
//       tertiary: {
//         color: '#4C9689',
//         hover: {
//           color: 'white'
//         }
//       },
//       danger: red,
//       info: blue,
//       warning: orange
//     },
//     typography: {
//       htmlFontSize: 15,
//       fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif'
//     },
//     body1: {
//       margin: 0
//     }
//   });
// }

function theme() {
  return createMuiTheme({
    palette: {
      primary: {
        ...teal,
        [primaryCode]: '#282e3f', // test color to remove.
        light: '#cac4c9',
        dark: '#1e222d',
        dark2: '#12151f'
      },
      secondary: grey,
      tertiary: {
        color: '#de9100',
        hover: {
          color: 'white'
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
      htmlFontSize: 15,
      fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif'
    },
    body1: {
      margin: 0
    }
  });
}

export default theme;