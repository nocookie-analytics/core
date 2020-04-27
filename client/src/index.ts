import Fingerprint2, {Component} from 'fingerprintjs2';
import objectHash from 'object-hash';

const getComponents = () => {
    Fingerprint2.getPromise().then(handleComponents);
};

const handleComponents = (components: Component[]) => {
  const userIdentifier: string = objectHash(components);
  console.log(userIdentifier);
};

if (window.requestIdleCallback) {
    requestIdleCallback(getComponents);
} else {
    setTimeout(getComponents, 500);
}
