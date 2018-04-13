// @flow

import React from 'react';
import { connect } from 'react-redux';

import DetailsApp from './DetailsApp';
import SearchApp from './SearchApp';
import ReplyApp from './ReplyApp';
import { CONTENTS_IDS } from '.';

const ChatAppRight = (props) => {
  const { componentId } = props;
  switch (componentId) {
  case CONTENTS_IDS.search:
    return <SearchApp {...props} />;
  case CONTENTS_IDS.reply:
    return <ReplyApp {...props} reverted customScrollbar dynamicDivider={false} />;
  default:
    return <DetailsApp {...props} />;
  }
};

export const mapStateToProps = (state) => {
  return {
    componentId: state.apps.chatApp.right.componentId
  };
};

export default connect(mapStateToProps)(ChatAppRight);