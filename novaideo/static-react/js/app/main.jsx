/* eslint-disable react/no-did-mount-set-state */
// @flow
import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { MuiThemeProvider, createGenerateClassName, jssPreset } from 'material-ui/styles';
import { withApollo, graphql } from 'react-apollo';
import withWidth from 'material-ui/utils/withWidth';
import { create } from 'jss';
import JssProvider from 'react-jss/lib/JssProvider';

import App from './app';
import { siteQuery } from './graphql/queries';
import { SMALL_WIDTH } from './constants';
import {
  userLogin,
  logout,
  updateUserToken,
  setConnectionState,
  loadAdapters,
  updateGlobalProps,
  updateNavigation
} from './actions/actions';
import { getCurrentLocation } from './utils/routeMap';
import { getActions } from './utils/processes';

const styleNode = document.createComment('insertion-point-jss');
// $FlowFixMe
document.head.insertBefore(styleNode, document.head.firstChild);

const generateClassName = createGenerateClassName({
  productionPrefix: 'n-i'
});
const jss = create(jssPreset());
jss.options.insertionPoint = 'insertion-point-jss';

class Main extends React.Component {
  state: { requirementsLoaded: boolean };

  static childContextTypes = {
    shortcuts: PropTypes.object.isRequired
  };

  constructor(props: any) {
    super(props);
    this.state = {
      requirementsLoaded: false
    };
  }

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

  componentWillReceiveProps(nextProps) {
    const { data, width, navigation } = nextProps;
    if (data.root) {
      this.props.updateGlobalProps({
        site: data.root,
        rootActions: getActions(
          data.actions.edges.map((action) => {
            return action.node;
          })
        ),
        smallScreen: SMALL_WIDTH.includes(width)
      });
      this.props.loadAdapters(data.root.siteId);
      const currentLocation = getCurrentLocation();
      if (navigation.location !== currentLocation) {
        this.props.updateNavigation(currentLocation, true);
      }
    }
  }

  componentWillUnmount() {
    // NetInfo.isConnected.removeEventListener('connectionChange', this.handleConnectionChange);
  }

  handleConnectionChange = (isConnected: boolean) => {
    this.props.setConnectionState(isConnected);
  };

  render() {
    const { data, theme } = this.props;

    if (data.loading) return null;
    const loged = true;

    return (
      <JssProvider jss={jss} generateClassName={generateClassName}>
        <MuiThemeProvider theme={theme}>
          <div className="main">
            {loged
              ? <App params={this.props.params}>
                {this.props.children}
              </App>
              : 'login'}
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
  logout: logout,
  loadAdapters: loadAdapters,
  updateUserToken: updateUserToken,
  updateGlobalProps: updateGlobalProps,
  updateNavigation: updateNavigation
};

export default withWidth()(
  withApollo(
    connect(mapStateToProps, mapDispatchToProps)(
      graphql(siteQuery, {
        options: (props: any) => {
          return {
            fetchPolicy: 'cache-first'
          };
        }
      })(Main)
    )
  )
);