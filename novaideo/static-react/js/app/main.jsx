/* eslint-disable react/no-did-mount-set-state */
import React from 'react';
import { connect } from 'react-redux';
import { MuiThemeProvider, createGenerateClassName, jssPreset } from '@material-ui/core/styles';
import { withApollo, graphql } from 'react-apollo';
import withWidth from '@material-ui/core/withWidth';
import { create } from 'jss';
import JssProvider from 'react-jss/lib/JssProvider';

import App from './app';
import SiteData from './graphql/queries/SiteData.graphql';
import { SMALL_WIDTH, AUTHORIZED_VIEWS } from './constants';
import { userLogin, userLogout, updateUserToken } from './actions/authActions';
import {
  setConnectionState, loadAdapters, updateGlobalProps, updateNavigation
} from './actions/instanceActions';
import { closeDrawer } from './actions/collaborationAppActions';
import { getCurrentLocation, getViewName } from './utils/routeMap';
import { getActions } from './utils/processes';
import { getTheme } from './theme';
import { setInputValue } from './utils/globalFunctions';
import LoginHome from './components/forms/processes/userProcess/LoginHome';

const styleNode = document.createComment('insertion-point-jss');
// $FlowFixMe
document.head.insertBefore(styleNode, document.head.firstChild);

const generateClassName = createGenerateClassName({
  productionPrefix: 'ni'
});
const jss = create(jssPreset());
jss.options.insertionPoint = 'insertion-point-jss';

class Main extends React.Component {
  constructor(props) {
    super(props);
    // TODO
    this.state = {
      requirementsLoaded: true
    };
  }

  // $FlowFixMe
  async componentDidMount() {
    // we need the connection status
    // const isConnected = await NetInfo.isConnected.fetch();
    const isConnected = true;
    // NetInfo.isConnected.addEventListener('connectionChange', this.handleConnectionChange);
    const { user, network, client } = this.props;
    // connect the user if he is not logged in (only if online).
    // When Offline mode is enabled (isConnected === false), we must display all of stored data
    // const historyEntry = history[instance.id];
    // let token = historyEntry ? historyEntry.data.token : user.token;
    // token = token || user.token;
    const { token } = user;
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

  componentWillReceiveProps(nextProps) {
    const {
      data, width, navigation, user, client
    } = nextProps;
    if (!data.loading && !data.error) {
      const { root, account, actions } = data;
      const smallScreen = SMALL_WIDTH.includes(width);
      this.props.updateGlobalProps({
        site: root,
        account: account,
        rootActions: getActions(
          actions
            && actions.edges.map((action) => {
              return action.node;
            })
        ),
        smallScreen: smallScreen
      });
      const accountId = account ? account.id : 'anonymous';
      setInputValue('execution-id', `${root.id}-${accountId}`);
      this.props.loadAdapters(root.siteId);
      const currentLocation = getCurrentLocation();
      if (navigation.location !== currentLocation) {
        this.props.updateNavigation(currentLocation, true);
      }
      if (smallScreen) this.props.closeDrawer();
      if (user.token !== this.props.user.token) {
        client.resetStore();
      }
    }
  }

  componentWillUnmount() {
    // NetInfo.isConnected.removeEventListener('connectionChange', this.handleConnectionChange);
  }

  handleConnectionChange = (isConnected) => {
    this.props.setConnectionState(isConnected);
  };

  render() {
    const {
      data, network, theme, children, params
    } = this.props;
    const { requirementsLoaded } = this.state;
    const { root, account } = data;
    if (!requirementsLoaded || data.loading || !root) return null;
    const userPreferencesTheme = account && account.preferences && account.preferences.theme;
    const themeToUse = (userPreferencesTheme && getTheme(userPreferencesTheme)) || theme;
    const viewName = getViewName();
    return (
      <JssProvider jss={jss} generateClassName={generateClassName}>
        <MuiThemeProvider theme={themeToUse}>
          <div className="main">
            {network.isLogged || !root.onlyForMembers ? (
              <App params={params}>{children}</App>
            ) : (
              <React.Fragment>
                <LoginHome />
                {AUTHORIZED_VIEWS.includes(viewName) ? children : null}
              </React.Fragment>
            )}
          </div>
        </MuiThemeProvider>
      </JssProvider>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    user: state.user,
    theme: state.adapters.theme,
    network: state.network,
    navigation: state.history.navigation
  };
};

export const mapDispatchToProps = {
  setConnectionState: setConnectionState,
  userLogin: userLogin,
  logout: userLogout,
  loadAdapters: loadAdapters,
  updateUserToken: updateUserToken,
  updateGlobalProps: updateGlobalProps,
  updateNavigation: updateNavigation,
  closeDrawer: closeDrawer
};

export default withWidth()(
  withApollo(
    connect(mapStateToProps, mapDispatchToProps)(
      graphql(SiteData, {
        options: () => {
          return {
            fetchPolicy: 'cache-and-network'
          };
        }
      })(Main)
    )
  )
);