// @flow
import * as React from 'react';
import classNames from 'classnames';

import { DEFAULT_EMBED_DATA } from '../../forms/widgets/mediumEditor/constants';
import URLMetadataLoader from '../urlPreview/URLMetadataLoader';

type Props = {
  url: string,
  size?: string,
  position?: string,
  caption?: ?string,
  afterLoad?: Function
};

const Url = ({
  url, size, position, caption, afterLoad
}: Props) => {
  return (
    <div
      className={classNames(
        'md-block-with-data',
        position || DEFAULT_EMBED_DATA.position,
        `size-${size || DEFAULT_EMBED_DATA.size}`
      )}
    >
      <URLMetadataLoader integreted key={`url-preview-${url}`} url={url} afterLoad={afterLoad} />
      {caption ? (
        <figcaption>
          <div>{caption}</div>
        </figcaption>
      ) : null}
    </div>
  );
};

Url.defaultProps = {
  size: DEFAULT_EMBED_DATA.size,
  position: DEFAULT_EMBED_DATA.position,
  afterLoad: null,
  caption: null
};

export default Url;