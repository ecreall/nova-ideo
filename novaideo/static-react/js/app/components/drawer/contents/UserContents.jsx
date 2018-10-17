/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import StorageIcon from '@material-ui/icons/Storage';
import { I18n } from 'react-redux-i18n';

import ContentItem from './ContentItem';
import ContentCollapse from '../../common/ContentCollapse';
import FlatList from '../../common/FlatList';
import MyContents from '../../../graphql/queries/MyContents.graphql';

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

export const DumbUserContents = ({
  classes, onOpen, id, open
}) => {
  return (
    <Query notifyOnNetworkStatusChange fetchPolicy="cache-and-network" query={MyContents} variables={{ first: 20, after: '' }}>
      {(result) => {
        const { data } = result;
        const totalCount = data && data.account && data.account.contents.totalCount;
        return (
          <ContentCollapse
            id={id}
            onOpen={onOpen}
            open={open}
            title={(
              <span>
                <span>{I18n.t('user.myContents')}</span>
                <span className={classes.counter}>{totalCount && `(${totalCount})`}</span>
              </span>
            )}
            Icon={StorageIcon}
          >
            <FlatList
              customScrollbar
              data={result}
              getEntities={(entities) => {
                return entities.data ? entities.data.account && entities.data.account.contents : entities.account.contents;
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

export default withStyles(styles)(DumbUserContents);