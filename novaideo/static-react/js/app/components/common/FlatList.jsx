/* eslint-disable no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import CircularProgress from '@material-ui/core/CircularProgress';
import debounce from 'lodash.debounce';

import { setURLState } from '../../actions/instanceActions';
import VirtualizedListItem from './VirtualizedListItem';
import { APOLLO_NETWORK_STATUS } from '../../constants';
import Scrollbar from './Scrollbar';
import { createEvent } from '../../utils/globalFunctions';

const styles = {
  progress: {
    position: 'relative',
    textAlign: 'center',
    padding: 20
  },
  moreBtn: {
    cursor: 'pointer',
    fontSize: 15,
    textAlign: 'center',
    margin: 10,
    lineHeight: 2.5,
    color: '#0576b9',
    '&:hover': {
      color: '#005e99',
      textDecoration: 'underline'
    }
  },
  revertedLisContainer: {
    display: 'flex',
    flexDirection: 'column-reverse',
    justifyContent: 'flex-end',
    minHeight: '100%'
  },
  footer: {
    justifyContent: 'space-between'
  },
  reverted: {
    display: 'flex',
    flexDirection: 'column-reverse'
  }
};

function emptyContainer({ children }) {
  return children;
}

function scrollbarContainer({
  children, handleScroll, scrollEvent, reverted, classes
}) {
  return (
    <Scrollbar
      scrollEvent={scrollEvent}
      reverted={reverted}
      classes={{
        scroll: classes.scroll,
        thumbVertical: classes.thumbVertical,
        trackVertical: classes.trackVertical
      }}
      onScroll={handleScroll}
    >
      {children}
    </Scrollbar>
  );
}

function virtualizedItemContainer({ itemHeightEstimation, children }) {
  return <VirtualizedListItem itemHeightEstimation={itemHeightEstimation}>{children}</VirtualizedListItem>;
}

export class DumbFlatList extends React.Component {
  static defaultProps = {
    virtualized: false,
    onEndReachedThreshold: 0.7,
    progressStyle: { size: 30 }
  };

  componentDidMount() {
    const { fetchMoreOnEvent, customScrollbar, moreBtn } = this.props;
    if (!moreBtn && (fetchMoreOnEvent || !customScrollbar)) {
      const event = fetchMoreOnEvent || 'scroll';
      document.addEventListener(event, this.handleScroll);
    }
  }

  componentWillReceiveProps(nextProps) {
    if (!nextProps.data.loading) {
      createEvent('resize', true);
    }
  }

  shouldComponentUpdate(nextProps) {
    const { data, getEntities } = nextProps;
    const preveData = this.props.data;
    if (!this.loading || data.loading || preveData.loading) return true;
    return getEntities(data).edges.length !== getEntities(preveData).edges.length;
  }

  componentWillUpdate(nextProps) {
    const {
      data, filter, network, getEntities, offlineFilter
    } = nextProps;
    let entities;
    let offlineStatus = false;
    try {
      if (data.error || !network.isConnected || network.url.error) {
        const dataEntities = getEntities(data);
        offlineStatus = true;
        if (!filter) {
          entities = dataEntities.edges;
        } else {
          const words = filter
            .toLowerCase()
            .split(' ')
            .filter((item) => {
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

  componentWillUnmount() {
    const { fetchMoreOnEvent, customScrollbar, moreBtn } = this.props;
    if (!moreBtn && (fetchMoreOnEvent || !customScrollbar)) {
      const event = fetchMoreOnEvent || 'scroll';
      document.removeEventListener(event, this.handleScroll);
    }
  }

  offline = {
    entities: undefined,
    status: false
  };

  loading = false;

  loadingDebounce = null;

  endReached = ({ scrollTop, scrollHeight, clientHeight }) => {
    const { onEndReachedThreshold, reverted } = this.props;
    const pad = onEndReachedThreshold * clientHeight;
    if (reverted) {
      const t = (scrollTop - pad) / (scrollHeight - clientHeight);
      if (t !== Infinity && t < 0) return true;
    } else {
      const t = (scrollTop + pad) / (scrollHeight - clientHeight);
      if (t !== Infinity && t > 1) return true;
    }
    return false;
  };

  handleScroll = (event) => {
    const {
      data, customScrollbar, getEntities, scrollEvent
    } = this.props;
    if (!customScrollbar && scrollEvent) createEvent(scrollEvent, true);
    if (getEntities(data).pageInfo.hasNextPage) {
      if (this.loadingDebounce) this.loadingDebounce.cancel();
      const loadNextData = () => {
        if (!this.loading && this.endReached(event.values || event)) {
          this.fetchMore();
        }
      };
      this.loadingDebounce = debounce(loadNextData, 20);
      this.loadingDebounce();
    }
  };

  fetchMore = () => {
    // The fetchMore method is used to load new data and add it
    // to the original query we used to populate the list
    const { data, network, getEntities } = this.props;
    // If no request is in flight for this query, and no errors happened. Everything is OK.
    const dataEntities = getEntities(data);
    if (data.networkStatus === APOLLO_NETWORK_STATUS.ready) {
      this.loading = true;
      data
        .fetchMore({
          variables: { after: dataEntities.pageInfo.endCursor || '' },
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
          this.loading = false;
          createEvent('resize', true);
        })
        .catch((e) => {
          if (!network.url.error) this.props.setURLState(true, [e.message]);
          this.loading = false;
        });
    }
  };

  onRefresh = () => {
    const { data, network } = this.props;
    data
      .refetch()
      .then(() => {
        if (network.url.error) this.props.setURLState(false, []);
      })
      .catch((e) => {
        if (!network.url.error) this.props.setURLState(true, [e.message]);
      });
  };

  setOfflineData = (entities, status, hasError, network) => {
    this.offline = { entities: entities, status: status };
    if (hasError && !network.url.error) {
      this.props.setURLState(true, []);
    }
  };

  renderProgress = () => {
    const { progressStyle, theme, classes } = this.props;
    const progressColor = progressStyle.color || theme.palette.primary[500];
    return (
      <div className={classes.progress}>
        <CircularProgress size={progressStyle.size} style={{ color: progressColor }} />
      </div>
    );
  };

  render() {
    const {
      data,
      getEntities,
      ListItem,
      Divider,
      itemProps,
      dividerProps,
      virtualized,
      itemHeightEstimation,
      customScrollbar,
      reverted,
      moreBtn,
      Footer,
      NoItems,
      scrollEvent,
      className,
      classes
    } = this.props;
    if (data.error) {
      // the fact of checking data.error remove the Unhandled (in react-apollo)
      // ApolloError error when the graphql server is down
      // Do nothing
    }
    const items = getEntities(data);
    const { networkStatus } = data;
    if (!items) {
      return this.renderProgress();
    }
    const { offline } = this;
    const entities = offline.status ? offline.entities : items.edges;
    const ScrollContainer = customScrollbar ? scrollbarContainer : emptyContainer;
    const ItemContainer = virtualized ? virtualizedItemContainer : emptyContainer;
    const hasItems = entities && entities.length > 0;
    return (
      <div className={className}>
        <ScrollContainer
          classes={classes}
          handleScroll={!moreBtn && this.handleScroll}
          reverted={reverted}
          scrollEvent={scrollEvent}
        >
          <div
            className={classNames({
              [classes.footer]: !!Footer,
              [classes.revertedLisContainer]: reverted
            })}
          >
            <div className={reverted && classes.reverted}>
              {hasItems
                ? entities.map((item, index) => {
                  const previous = entities[index - 1];
                  const next = entities[index + 1];
                  const result = [
                    <ItemContainer key="item-container" itemHeightEstimation={itemHeightEstimation}>
                      <ListItem
                        reverted={reverted}
                        index={index}
                        node={item.node}
                        next={next && next.node}
                        previous={previous && previous.node}
                        itemProps={itemProps}
                      />
                    </ItemContainer>
                  ];
                  if (Divider) {
                    const divider = (
                      <Divider
                        key="divider"
                        reverted={reverted}
                        index={index}
                        node={item.node}
                        eventId={scrollEvent}
                        next={next && next.node}
                        previous={previous && previous.node}
                        dividerProps={{ ...dividerProps, ...itemProps }}
                      />
                    );
                    if (reverted) {
                      result.push(divider);
                    } else {
                      result.unshift(divider);
                    }
                  }
                  return result;
                })
                : null}
              {networkStatus === APOLLO_NETWORK_STATUS.fetchMore && items.pageInfo.hasNextPage && this.renderProgress()}
              {networkStatus !== APOLLO_NETWORK_STATUS.fetchMore
                && items.pageInfo.hasNextPage
                && moreBtn && (
                <div className={classes.moreBtn} onClick={this.fetchMore}>
                  {moreBtn}
                </div>
              )}
            </div>
            <div>
              {Footer && !items.pageInfo.hasNextPage ? <Footer data={data} /> : null}
              {NoItems && !hasItems ? <NoItems data={data} /> : null}
            </div>
          </div>
        </ScrollContainer>
      </div>
    );
  }
}

export const mapStateToProps = (state) => {
  return { network: state.network, filter: state.search.text };
};

export const mapDispatchToProps = { setURLState: setURLState };

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(DumbFlatList));