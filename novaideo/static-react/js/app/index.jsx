import 'babel-polyfill';
import React from 'react';
import { Provider } from 'react-redux';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import { Router, browserHistory } from 'react-router';
import { ApolloProvider } from 'react-apollo';
import { PersistGate } from 'redux-persist/integration/react';

import createAppStore from './store';
import getApolloClient from './client';
import Routes from './routes';
import hashLinkScroll from './utils/hashLinkScroll';

require('smoothscroll-polyfill').polyfill();

const storeData = createAppStore();

const renderRoutes = (routes) => {
  ReactDOM.render(
    <AppContainer>
      <ApolloProvider client={getApolloClient(storeData.store)}>
        <Provider store={storeData.store}>
          <PersistGate loading={null} persistor={storeData.persistor}>
            <Router history={browserHistory} routes={routes} onUpdate={hashLinkScroll} />
          </PersistGate>
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