import React from 'react';
import { Route, IndexRoute } from 'react-router';
import Main from './main';
import Home from './components/collaborationApp/Home';

export default [
  <Route path="/" component={Main}>
    <IndexRoute component={Home} />
    <Route path="/messages/:channelId" component={Home} />
    <Route path="/ideas/:ideaId" component={Home} />
  </Route>
];