import React from 'react';
import Typography from '@material-ui/core/Typography';
import { connect } from 'react-redux';

import IdeasList from './IdeasList';
import CreateIdeaHome from '../idea/CreateIdeaHome';
import { MAIN_SEARCH_ID, MAIN_FILTER_ID } from '../../constants';

export const DumbHome = ({ filter }) => {
  return (
    <Typography component="div">
      {!filter || !filter.text ? <CreateIdeaHome /> : null}
      <IdeasList searchId={MAIN_SEARCH_ID} filterId={MAIN_FILTER_ID} />
    </Typography>
  );
};

export const mapStateToProps = (state) => {
  return {
    filter: state.search[MAIN_SEARCH_ID]
  };
};

export default connect(mapStateToProps)(DumbHome);