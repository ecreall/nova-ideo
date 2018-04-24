/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';

import IdeaItem from '../idea/IdeaItem';
import FlatList from '../common/FlatList';
import IdeasList from '../../graphql/queries/IdeasList.graphql';
import Divider from './Divider';
import { ACTIONS } from '../../processes';
import SearchData from '../common/SearchData';

const styles = {
  list: {
    backgroundColor: 'white',
    border: 'solid 1px #8080802e',
    borderTop: 'none'
  }
};

export const DumbIdeasList = ({ filter, searchId, classes }) => {
  return (
    <Query
      notifyOnNetworkStatusChange
      fetchPolicy="cache-and-network"
      query={IdeasList}
      variables={{
        first: 15,
        after: '',
        filter: filter,
        processIds: [],
        nodeIds: [],
        processTags: [],
        actionTags: [ACTIONS.primary]
      }}
    >
      {(result) => {
        const totalCount = result.data && result.data.ideas && result.data.ideas.totalCount;
        return [
          filter ? <SearchData id={searchId} count={totalCount} /> : null,
          <FlatList
            scrollEvent="ideas"
            data={result}
            getEntities={(entities) => {
              return entities.data ? entities.data.ideas : entities.ideas;
            }}
            ListItem={IdeaItem}
            Divider={Divider}
            className={classes.list}
          />
        ];
      }}
    </Query>
  );
};

export const mapStateToProps = (state, props) => {
  const searchId = props.searchId;
  return {
    filter: state.search[searchId] ? state.search[searchId].text : ''
  };
};

export default withStyles(styles)(connect(mapStateToProps)(DumbIdeasList));