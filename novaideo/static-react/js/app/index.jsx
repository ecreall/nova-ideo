import 'babel-polyfill';
import React from 'react';
import { Provider } from 'react-redux';
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

const renderRoutes = (routes) => {
  ReactDOM.render(
    <AppContainer>
      <ApolloProvider client={getApolloClient(store)}>
        <Provider store={store}>
          <Router history={browserHistory} routes={routes} onUpdate={hashLinkScroll} />
        </Provider>
      </ApolloProvider>
    </AppContainer>,
    document.getElementById('root')
  );
};

renderRoutes(Routes);

// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('./routes', () => {
    const NewRoutes = require('./routes').default; // eslint-disable-line
    renderRoutes(NewRoutes);
  });
}