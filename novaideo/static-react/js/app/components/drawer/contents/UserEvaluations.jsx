/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import SwapVerticalCircleIcon from '@material-ui/icons/SwapVerticalCircle';
import { I18n } from 'react-redux-i18n';

import ContentItem from './ContentItem';
import ContentCollapse from '../../common/ContentCollapse';
import FlatList from '../../common/FlatList';
import MySupports from '../../../graphql/queries/MySupports.graphql';

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

export const DumbUserEvaluations = ({ classes, onOpen, id, open }) => {
  return (
    <Query notifyOnNetworkStatusChange fetchPolicy="cache-and-network" query={MySupports} variables={{ first: 20, after: '' }}>
      {(result) => {
        const { data } = result;
        const totalCount = data && data.account && data.account.supportedIdeas.totalCount;
        return (
          <ContentCollapse
            id={id}
            onOpen={onOpen}
            open={open}
            title={
              <span>
                <span>
                  {I18n.t('user.myEvaluations')}
                </span>
                <span className={classes.counter}>
                  {totalCount && `(${totalCount})`}
                </span>
              </span>
            }
            Icon={SwapVerticalCircleIcon}
          >
            <FlatList
              customScrollbar
              data={result}
              getEntities={(entities) => {
                return entities.data
                  ? entities.data.account && entities.data.account.supportedIdeas
                  : entities.account.supportedIdeas;
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

export default withStyles(styles)(DumbUserEvaluations);