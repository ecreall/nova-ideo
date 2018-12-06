// @flow
import * as React from 'react';
import classNames from 'classnames';

import { DEFAULT_EMBED_DATA } from '../../forms/widgets/mediumEditor/constants';

type Props = {
  src: string,
  size?: string,
  position?: string,
  caption?: string
};

const Image = ({
  src, size, position, caption
}: Props) => {
  return (
    <div
      className={classNames(
        'md-block-with-data',
        position || DEFAULT_EMBED_DATA.position,
        `size-${size || DEFAULT_EMBED_DATA.size}`
      )}
    >
      <div className="md-block-image-inner-container">
        <img alt="text-block" src={src} />
      </div>
      {caption ? (
        <figcaption>
          <div>{caption}</div>
        </figcaption>
      ) : null}
    </div>
  );
};

Image.defaultProps = {
  size: DEFAULT_EMBED_DATA.size,
  position: DEFAULT_EMBED_DATA.position,
  caption: null
};

export default Image;