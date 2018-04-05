import React from 'react';
import { connect } from 'react-redux';

import ChatApp from './ChatApp';
import { CONTENTS_IDS } from '.';

const CollaborationAppRight = (props) => {
  const { componentId } = props;
  if (componentId === CONTENTS_IDS.chat) return <ChatApp {...props} />;
  return null;
};

export const mapStateToProps = (state) => {
  return {
    componentId: state.apps.collaborationApp.right.componentId
  };
};

export default connect(mapStateToProps)(CollaborationAppRight);