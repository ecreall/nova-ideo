// @flow
import React from 'react';

import { getUrls } from '../../../utils/linkify';
import URLMetadataLoader from './URLMetadataLoader';

type Props = {
  body: string,
  className: string
};

const URLs = (props: Props) => {
  const { body, className } = props;
  // We need to add the URLs previews to the end of each post (See URLMetadataLoader)
  const urls = body ? Array.from(new Set([...getUrls(body)])) : [];
  if (urls.length === 0) return null;
  return (
    <div className={className}>
      {urls.map((url) => {
        return <URLMetadataLoader key={url} url={url} />;
      })}
    </div>
  );
};

export default URLs;