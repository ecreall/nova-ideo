/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import StorageIcon from 'material-ui-icons/Storage';
import { I18n } from 'react-redux-i18n';

import ContentItem from './ContentItem';
import ContentCollapse from '../common/ContentCollapse';
import EntitiesList from '../common/EntitiesList';
import { myContentsQuery } from '../../graphql/queries';

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

export class DumbUserContents extends React.Component {
  render() {
    const { data, classes, onOpen, id, open } = this.props;
    const totalCount = data.account && data.account.contents.totalCount;
    return (
      <ContentCollapse
        id={id}
        onOpen={onOpen}
        open={open}
        title={
          <span>
            <span>
              {I18n.t('user.myContents')}
            </span>
            <span className={classes.counter}>
              {totalCount && `(${totalCount})`}
            </span>
          </span>
        }
        Icon={StorageIcon}
      >
        <EntitiesList
          customScrollbar
          data={data}
          getEntities={(entities) => {
            return entities.account && entities.account.contents;
          }}
          ListItem={ContentItem}
          className={classes.list}
          progressStyle={{ size: 20, color: 'white' }}
          classes={{ thumbVertical: classes.thumbVertical }}
        />
      </ContentCollapse>
    );
  }
}

export default withStyles(styles)(
  graphql(myContentsQuery, {
    options: () => {
      return {
        fetchPolicy: 'cache-and-network',
        notifyOnNetworkStatusChange: true,
        variables: { first: 20, after: '' }
      };
    }
  })(DumbUserContents)
);