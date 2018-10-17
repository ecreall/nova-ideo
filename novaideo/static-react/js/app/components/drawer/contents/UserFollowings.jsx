/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import StarIcon from '@material-ui/icons/Star';
import { I18n } from 'react-redux-i18n';

import ContentItem from './ContentItem';
import ContentCollapse from '../../common/ContentCollapse';
import FlatList from '../../common/FlatList';
import MyFollowings from '../../../graphql/queries/MyFollowings.graphql';

const styles = {
  list: {
    height: '100%'
  },
  counter: {
    fontFamily: 'LatoWebLight',
    fontWeight: 100,
    marginLeft: 5,
    fontSize: 14
  },
  thumbVertical: {
    backgroundColor: 'rgba(255, 255, 255, 0.22)',
    border: 'none'
  }
};

export const DumbUserFollowings = ({
  classes, onOpen, id, open
}) => {
  return (
    <Query notifyOnNetworkStatusChange fetchPolicy="cache-and-network" query={MyFollowings} variables={{ first: 20, after: '' }}>
      {(result) => {
        const { data } = result;
        const totalCount = data && data.account && data.account.followedIdeas.totalCount;
        return (
          <ContentCollapse
            id={id}
            onOpen={onOpen}
            open={open}
            title={(
              <span>
                <span>{I18n.t('user.myFollowings')}</span>
                <span className={classes.counter}>{totalCount && `(${totalCount})`}</span>
              </span>
            )}
            Icon={StarIcon}
          >
            <FlatList
              customScrollbar
              data={result}
              getEntities={(entities) => {
                return entities.data
                  ? entities.data.account && entities.data.account.followedIdeas
                  : entities.account.followedIdeas;
              }}
              ListItem={ContentItem}
              className={classes.list}
              progressStyle={{ size: 20, color: 'white' }}
              classes={{ thumbVertical: classes.thumbVertical }}
            />
          </ContentCollapse>
        );
      }}
    </Query>
  );
};

export default withStyles(styles)(DumbUserFollowings);