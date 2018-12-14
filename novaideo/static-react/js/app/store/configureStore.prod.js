import { createStore, applyMiddleware, compose } from 'redux';
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = {
  key: 'NovaIdeo',
  storage: storage,
  blacklist: ['i18n', 'network', 'adapters', 'search', 'filter', 'apps']
};

export default function configureStore(initialState, rootReducer, middlewares) {
  return createStore(persistReducer(persistConfig, rootReducer), initialState, compose(applyMiddleware(...middlewares)));
}