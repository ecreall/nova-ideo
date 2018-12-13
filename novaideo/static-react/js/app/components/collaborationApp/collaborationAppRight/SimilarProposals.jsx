/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';
import Icon from '@material-ui/core/Icon';
import { connect } from 'react-redux';
import classNames from 'classnames';
import { Query } from 'react-apollo';

import RightContent from './RightContent';
import IdeaItem from '../../idea/IdeaItem';
import FlatList from '../../common/FlatList';
import IdeasList from '../../../graphql/queries/IdeasList.graphql';
import { ACTIONS } from '../../../processes';

const styles = {
  appTitle: {
    marginLeft: 10
  },
  appIcon: {
    fontWeight: '900 !important',
    fontSize: '16px !important',
    marginRight: 5
  }
};

export const DumbSimilarProposals = ({
  classes, appProps: {
    title, canExpand, filter, generateFilter
  }
}) => {
  return (
    <RightContent
      title={(
        <div className={classes.appTitle}>
          <Icon className={classNames('mdi-set mdi-lightbulb', classes.appIcon)} />
          {title}
        </div>
      )}
      canExpand={canExpand}
    >
      <Query
        notifyOnNetworkStatusChange
        fetchPolicy="cache-and-network"
        query={IdeasList}
        variables={{
          first: 15,
          after: '',
          filter: filter,
          generateFilter: generateFilter,
          processIds: [],
          nodeIds: [],
          processTags: [],
          actionTags: [ACTIONS.primary]
        }}
      >
        {(result) => {
          return (
            <FlatList
              moreBtn={<span>{I18n.t('common.moreResult')}</span>}
              data={result}
              getEntities={(entities) => {
                return entities.data ? entities.data.ideas : entities.ideas;
              }}
              ListItem={IdeaItem}
            />
          );
        }}
      </Query>
    </RightContent>
  );
};

export const mapStateToProps = (state) => {
  return {
    appProps: state.apps.collaborationApp.right.props
  };
};

export default withStyles(styles)(connect(mapStateToProps)(DumbSimilarProposals));