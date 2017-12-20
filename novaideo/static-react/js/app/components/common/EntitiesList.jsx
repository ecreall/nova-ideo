/* eslint-disable no-undef */
import React from 'react';
import { connect } from 'react-redux';

import Loader from './Loader';

export class DumbEntitiesList extends React.Component {
  constructor(props) {
    super(props);
    this.offline = {
      entities: undefined,
      status: false
    };
    this.onEndReached = this.onEndReached.bind(this);
    this.onRefresh = this.onRefresh.bind(this);
    this.setOfflineData = this.setOfflineData.bind(this);
  }

  componentWillUpdate(nextProps) {
    const { data, filter, network, getEntities, offlineFilter } = nextProps;
    let entities;
    let offlineStatus = false;
    try {
      if (data.error || !network.isConnected || network.url.error) {
        const dataEntities = getEntities(data);
        offlineStatus = true;
        if (!filter) {
          entities = dataEntities.edges;
        } else {
          const words = filter.toLowerCase().split(' ').filter((item) => {
            return item;
          });
          entities = dataEntities.edges.filter((entity) => {
            return words
              .map((item) => {
                return offlineFilter(entity, item);
              })
              .includes(true);
          });
        }
      }
      this.setOfflineData(entities, offlineStatus);
    } catch (e) {
      this.setOfflineData(entities, offlineStatus, true, network);
    }
  }

  onEndReached() {
    // The fetchMore method is used to load new data and add it
    // to the original query we used to populate the list
    const { data, network, getEntities } = this.props;
    // If no request is in flight for this query, and no errors happened. Everything is OK.
    if (data.networkStatus === 7) {
      data
        .fetchMore({
          variables: { after: getEntities(data).pageInfo.endCursor || '' },
          updateQuery: (previousResult, { fetchMoreResult }) => {
            // Don't do anything if there weren't any new items
            const previousResultEntities = getEntities(previousResult);
            if (!fetchMoreResult || !previousResultEntities.pageInfo.hasNextPage) {
              return previousResult;
            }
            const fetchMoreResultEntities = getEntities(fetchMoreResult);
            fetchMoreResultEntities.edges = previousResultEntities.edges.concat(fetchMoreResultEntities.edges);
            return fetchMoreResult;
          }
        })
        .then(() => {
          if (network.url.error) this.props.setURLState(false, []);
        })
        .catch((e) => {
          if (!network.url.error) this.props.setURLState(true, [e.message]);
        });
    }
  }

  onRefresh() {
    const { data, network } = this.props;
    data
      .refetch()
      .then(() => {
        if (network.url.error) this.props.setURLState(false, []);
      })
      .catch((e) => {
        if (!network.url.error) this.props.setURLState(true, [e.message]);
      });
  }

  setOfflineData(entities, status, hasError, network) {
    this.offline = { entities: entities, status: status };
    if (hasError && !network.url.error) {
      this.props.setURLState(true, []);
    }
  }

  render() {
    const { data, ListItem, itemdata, getEntities } = this.props;
    if (data.error) {
      // the fact of checking data.error remove the Unhandled (in react-apollo)
      // ApolloError error when the graphql server is down
      // Do nothing
    }
    const dataEntities = getEntities(data);
    if (dataEntities == null || data.networkStatus === 1 || data.networkStatus === 2) {
      return (
        <div>
          <Loader textHidden />
        </div>
      );
    }
    const offline = this.offline;
    const entities = offline.status ? offline.entities : dataEntities.edges;
    return (
      <div>
        {entities && entities.length > 0
          ? <div>
            {entities.map((item) => {
              return <ListItem itemdata={itemdata} node={item.node} />;
            })}
          </div>
          : null}
      </div>
    );
  }
}

export const mapStateToProps = (state) => {
  return { network: state.network, filter: state.search.text };
};

export const mapDispatchToProps = {};

export default connect(mapStateToProps, mapDispatchToProps)(DumbEntitiesList);