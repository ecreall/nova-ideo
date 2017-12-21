import React from 'react';
import grey from 'material-ui/colors/grey';
import teal from 'material-ui/colors/teal';
import { MuiThemeProvider, createMuiTheme } from 'material-ui/styles';

import App from './app';

function theme() {
  return createMuiTheme({
    palette: {
      primary: teal, // Purple and green play nicely together.
      secondary: {
        ...grey
      }
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

class Main extends React.Component {
  render() {
    const loged = true;
    return (
      <MuiThemeProvider theme={theme}>
        <div className="main">
          {loged
            ? <App>
              {this.props.children}
            </App>
            : 'login'}
        </div>
      </MuiThemeProvider>
    );
  }
}

export default Main;