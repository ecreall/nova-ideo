/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import SwapVerticalCircleIcon from 'material-ui-icons/SwapVerticalCircle';
import { I18n } from 'react-redux-i18n';

import ContentItem from './ContentItem';
import ContentCollapse from '../common/ContentCollapse';
import EntitiesList from '../common/EntitiesList';
import { mySupportsQuery } from '../../graphql/queries';

const styles = {
  list: {
    height: '100%'
  },
  counter: {
    fontFamily: 'LatoWebLight',
    fontWeight: 100,
    marginLeft: 5,
    fontSize: 14
  }
};

export class DumbUserEvaluations extends React.Component {
  render() {
    const { data, classes, onOpen, id, open } = this.props;
    const totalCount = data.account && data.account.supportedIdeas.totalCount;
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
        <EntitiesList
          customScrollbar
          data={data}
          getEntities={(entities) => {
            return entities.account && entities.account.supportedIdeas;
          }}
          className={classes.list}
          itemHeightEstimation={30}
          progressStyle={{ size: 20, color: 'white' }}
          scrollbarStyle={{ thumbVertical: { backgroundColor: 'rgba(255, 255, 255, 0.22)' } }}
          ListItem={ContentItem}
        />
      </ContentCollapse>
    );
  }
}

export default withStyles(styles)(
  graphql(mySupportsQuery, {
    options: () => {
      return {
        fetchPolicy: 'cache-and-network',
        notifyOnNetworkStatusChange: true,
        variables: { first: 20, after: '' }
      };
    }
  })(DumbUserEvaluations)
);