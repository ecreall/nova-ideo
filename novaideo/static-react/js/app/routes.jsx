import React from 'react';
import { Route, IndexRoute } from 'react-router';
import Main from './main';
import Home from './components/views/Home';

export default [
  <Route path="/" component={Main}>
    <IndexRoute component={Home} />
  </Route>
];