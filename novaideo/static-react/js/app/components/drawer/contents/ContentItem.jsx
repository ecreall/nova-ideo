/* eslint-disable no-underscore-dangle */
import React from 'react';

import IdeaListingItem from './IdeaListingItem';

const ContentItem = (props) => {
  const { node } = props;
  switch (node.__typename) {
  case 'Idea':
    return <IdeaListingItem {...props} />;
  default:
    return null;
  }
};

export default ContentItem;