// @flow
import React from 'react';
import { Query } from 'react-apollo';

import UrlPreview from './URLPreview';
import URLMetadata from '../../../graphql/queries/URLMetadata.graphql';

type URLMetadataLoaderProps = {
  url: string,
  afterLoad: ?Function
};

class URLMetadataLoader extends React.Component<*, URLMetadataLoaderProps, void> {
  render() {
    const { afterLoad, url } = this.props;
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
          return metadata ? <UrlPreview {...metadata} afterLoad={afterLoad} /> : null;
        }}
      </Query>
    );
  }
}

export default URLMetadataLoader;