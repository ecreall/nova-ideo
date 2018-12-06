// @flow
import * as React from 'react';
import activeHtml from 'react-active-html';

import { transformLinksInHtml } from '../../../utils/linkify';
// import URLMetadataLoader from '../urlPreview/URLMetadataLoader';
// import Image from './Image';
import Url from './Url';

type Props = {
  html: string,
  containerRef: ?Function,
  replacementComponents?: (afterLoad?: Function) => Object,
  afterUrlLoad?: Function
};

export const defaultReplacementComponents = (afterLoad?: Function) => {
  return {
    figure: (attributes: Object) => {
      const { children } = attributes;
      const embed = children ? children[0] : null;
      if (!embed) return null;
      const { href } = embed.props;
      if (!href) return null;
      return <Url url={href} afterLoad={afterLoad} position={embed.props['data-position']} size={embed.props['data-size']} />;
    }
    // a: (attributes: Object) => {
    //   const {
    //     href, key, target, title, children, ...props
    //   } = attributes;
    //   return (
    //     <React.Fragment>
    //       <a {...props} key={`url-link-${key}`} href={href} className="linkified" target={target} title={title}>
    //         {children}
    //       </a>
    //       <URLMetadataLoader key={`url-preview-${href}`} url={href} afterLoad={afterLoad} />
    //     </React.Fragment>
    //   );
    // }
  };
};

const Html = ({
  html, containerRef, replacementComponents, afterUrlLoad, ...containerProps
}: Props) => {
  const replacementMapping = replacementComponents ? replacementComponents(afterUrlLoad) : null;
  const content = activeHtml(transformLinksInHtml(html), replacementMapping);
  return (
    <div ref={containerRef} {...containerProps}>
      {content}
    </div>
  );
};

Html.defaultProps = {
  replacementComponents: defaultReplacementComponents,
  afterUrlLoad: null
};

export default Html;