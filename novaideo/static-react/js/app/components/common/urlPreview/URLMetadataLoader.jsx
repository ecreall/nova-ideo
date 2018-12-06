// @flow
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';

import UrlPreview from './URLPreview';
import URLMetadata from '../../../graphql/queries/URLMetadata.graphql';

type URLMetadataLoaderProps = {
  url: string,
  afterLoad?: ?Function,
  integreted?: boolean,
  classes: { [string]: string },
  withLoader?: boolean
};

const styles = {
  progress: {
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }
};

class URLMetadataLoader extends React.Component<URLMetadataLoaderProps, void> {
  static defaultProps = {
    afterLoad: () => {},
    integreted: false,
    withLoader: false
  };

  render() {
    const {
      afterLoad, classes, url, integreted, withLoader
    } = this.props;
    return (
      <Query
        notifyOnNetworkStatusChange
        fetchPolicy="cache-and-network"
        query={URLMetadata}
        variables={{
          url: url
        }}
      >
        {(result) => {
          const metadata = result.data && result.data.metadata;
          const loader = withLoader ? (
            <div className={classes.progress}>
              <CircularProgress size={27} />
            </div>
          ) : null;
          return metadata ? <UrlPreview {...metadata} integreted={integreted} classes={classes} afterLoad={afterLoad} /> : loader;
        }}
      </Query>
    );
  }
}

export default withStyles(styles)(URLMetadataLoader);