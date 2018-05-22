import React from 'react';
import { Route } from 'react-router';
import Main from './main';
import Channel from './components/chatApp/Channel';
import Idea from './components/idea/Idea';
import User from './components/user/User';
import Login from './components/forms/processes/userProcess/Login';
import ConfirmRegistration from './components/forms/processes/userProcess/ConfirmRegistration';

export default [
  <Route path="/" component={Main}>
    <Route path="/registrations/:registrationId" component={ConfirmRegistration} />
    <Route path="/messages/:channelId" component={Channel} />
    <Route path="/ideas/:ideaId" component={Idea} />
    <Route path="/users/:userId" component={User} />
    <Route path="/login" component={Login} />
  </Route>
];