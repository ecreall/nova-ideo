/* eslint-disable react/no-did-mount-set-state */
// @flow
import React from 'react';
import { connect } from 'react-redux';
import { teal, grey, deepOrange, orange, blue } from 'material-ui/colors';
import { MuiThemeProvider, createMuiTheme } from 'material-ui/styles';
import { withApollo } from 'react-apollo';

import App from './app';
import { userLogin, logout, updateUserToken, setConnectionState } from './actions/actions';

const primaryCode = 500;

function theme() {
  return createMuiTheme({
    palette: {
      primary: {
        ...teal,
        [primaryCode]: '#3e313c' // test color to remove.
      },
      secondary: grey,
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

class Main extends React.Component {
  state: { requirementsLoaded: boolean };

  constructor(props: any) {
    super(props);
    this.state = {
      requirementsLoaded: false
    };
  }

  // componentWillMount() {
  //   if (this.props.instance.id) {
  //     // update adapters of the instance
  //     this.props.loadAdapters(this.props.instance.id);
  //   }
  // }

  // $FlowFixMe
  async componentDidMount() {
    // we need the connection status
    // const isConnected = await NetInfo.isConnected.fetch();
    const isConnected = true;
    // NetInfo.isConnected.addEventListener('connectionChange', this.handleConnectionChange);
    // await Font.loadAsync({
    //   'Roboto-Regular': FONTS.robotoRegular,
    //   'Roboto-Medium': FONTS.robotoMedium
    // });
    const { user, network, client } = this.props;
    // connect the user if he is not logged in (only if online).
    // When Offline mode is enabled (isConnected === false), we must display all of stored data
    // const historyEntry = history[instance.id];
    // let token = historyEntry ? historyEntry.data.token : user.token;
    // token = token || user.token;
    const token = user.token;
    if (isConnected && !network.isLogged && token) {
      const reset = () => {
        client.resetStore().then(() => {
          return this.setState({ requirementsLoaded: true });
          // return this.setState({ requirementsLoaded: true }, () => {
          //   return this.props.updateUserToken(newToken);
          // });
        });
      };
      this.props
        .userLogin('', '', token)
        .then(({ value }) => {
          // if login failed we must logout the user then update data. else we
          // need to update user data
          if (!value.status) {
            this.props.logout().then(reset);
          } else {
            // update the user token (see the history reducer)
            reset();
          }
        })
        .catch(() => {
          this.props.logout().then(reset);
        });
    } else {
      this.setState({ requirementsLoaded: true });
    }
    this.handleConnectionChange(isConnected);
  }

  componentWillUnmount() {
    // NetInfo.isConnected.removeEventListener('connectionChange', this.handleConnectionChange);
  }

  handleConnectionChange = (isConnected: boolean) => {
    this.props.setConnectionState(isConnected);
  };

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

const mapStateToProps = (state) => {
  return {
    user: state.user,
    network: state.network
    // adapters: state.adapters,
  };
};

export const mapDispatchToProps = {
  setConnectionState: setConnectionState,
  userLogin: userLogin,
  logout: logout,
  // loadAdapters: loadAdapters,
  updateUserToken: updateUserToken
  // updateGlobalProps: updateGlobalProps
};

export default connect(mapStateToProps, mapDispatchToProps)(withApollo(Main));