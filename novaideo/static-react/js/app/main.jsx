import React from 'react';
import lightBaseTheme from 'material-ui/styles/baseThemes/darkBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';

import App from './app';

class Main extends React.Component {
  render() {
    const loged = true;
    return (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
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