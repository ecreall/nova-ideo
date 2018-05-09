import React from 'react';
import Typography from 'material-ui/Typography';
import { connect } from 'react-redux';

import IdeasList from './IdeasList';
import CreateIdeaHome from '../idea/CreateIdeaHome';

export const DumbHome = ({ filter }) => {
  const hasFilter = filter && filter.text;
  const searchId = 'globalSearch';
  return (
    <Typography component="div">
      {!hasFilter && <CreateIdeaHome />}
      <IdeasList searchId={searchId} />
    </Typography>
  );
};

export const mapStateToProps = (state) => {
  return {
    filter: state.search.globalSearch
  };
};

export default connect(mapStateToProps)(DumbHome);