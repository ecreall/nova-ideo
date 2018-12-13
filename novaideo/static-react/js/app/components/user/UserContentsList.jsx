/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';

import IdeaItem from '../idea/IdeaItem';
import FlatList from '../common/FlatList';
import UserContents from '../../graphql/queries/UserContents.graphql';
import Divider from '../collaborationApp/Divider';
import { ACTIONS } from '../../processes';
import SearchData from '../common/SearchData';

const styles = {
  list: {
    backgroundColor: 'white',
    border: 'solid 1px #8080802e',
    borderTop: 'none'
  }
};

export const DumbUserContentsList = ({ id, filter, classes }) => {
  return (
    <Query
      notifyOnNetworkStatusChange
      fetchPolicy="cache-and-network"
      query={UserContents}
      variables={{
        first: 15,
        after: '',
        filter: filter,
        id: id,
        processIds: [],
        nodeIds: [],
        processTags: [],
        actionTags: [ACTIONS.primary]
      }}
    >
      {(result) => {
        const totalCount = result.data && result.data.person && result.data.person.contents.totalCount;
        return (
          <React.Fragment>
            {filter && filter.text ? <SearchData id={`${id}-search`} count={totalCount} /> : null}
            <FlatList
              fetchMoreOnEvent={`${id}user-contents`}
              // scrollEvent={`${id}user-contents`}
              data={result}
              getEntities={(entities) => {
                return entities.data ? entities.data.person && entities.data.person.contents : entities.person.contents;
              }}
              ListItem={IdeaItem}
              Divider={Divider}
              className={classes.list}
            />
          </React.Fragment>
        );
      }}
    </Query>
  );
};

export const mapStateToProps = (state, props) => {
  const searchId = `${props.id}-search`;
  return {
    filter: state.search[searchId] ? state.search[searchId] : {}
  };
};

export default withStyles(styles)(connect(mapStateToProps)(DumbUserContentsList));