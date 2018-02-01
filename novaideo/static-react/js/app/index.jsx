import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import { Router, browserHistory } from 'react-router';
import { ApolloProvider } from 'react-apollo';
import createAppStore from './store';
import getApolloClient from './client';
import Routes from './routes';
import hashLinkScroll from './utils/hashLinkScroll';

require('smoothscroll-polyfill').polyfill();

const store = createAppStore();

ReactDOM.render(
  <AppContainer>
    <ApolloProvider store={store} client={getApolloClient(store)}>
      <Router history={browserHistory} routes={Routes} onUpdate={hashLinkScroll} />
    </ApolloProvider>
  </AppContainer>,
  document.getElementById('root')
);

// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('./routes', () => {
    const NewRoutes = require('./routes').default; // eslint-disable-line
    ReactDOM.render(
      <AppContainer>
        <ApolloProvider store={store} client={getApolloClient(store)}>
          <Router history={browserHistory} routes={NewRoutes} onUpdate={hashLinkScroll} />
        </ApolloProvider>
      </AppContainer>,
      document.getElementById('root')
    );
  });
}