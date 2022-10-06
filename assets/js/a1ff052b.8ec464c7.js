"use strict";(self.webpackChunkmy_website=self.webpackChunkmy_website||[]).push([[804],{3905:(e,t,n)=>{n.d(t,{Zo:()=>s,kt:()=>d});var a=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var p=a.createContext({}),u=function(e){var t=a.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},s=function(e){var t=u(e.components);return a.createElement(p.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},m=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,i=e.originalType,p=e.parentName,s=l(e,["components","mdxType","originalType","parentName"]),m=u(n),d=r,k=m["".concat(p,".").concat(d)]||m[d]||c[d]||i;return n?a.createElement(k,o(o({ref:t},s),{},{components:n})):a.createElement(k,o({ref:t},s))}));function d(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=n.length,o=new Array(i);o[0]=m;var l={};for(var p in t)hasOwnProperty.call(t,p)&&(l[p]=t[p]);l.originalType=e,l.mdxType="string"==typeof e?e:r,o[1]=l;for(var u=2;u<i;u++)o[u]=n[u];return a.createElement.apply(null,o)}return a.createElement.apply(null,n)}m.displayName="MDXCreateElement"},9913:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>p,contentTitle:()=>o,default:()=>c,frontMatter:()=>i,metadata:()=>l,toc:()=>u});var a=n(7462),r=(n(7294),n(3905));const i={},o="Deploying to AWS",l={unversionedId:"deploying-your-app/deploying-code",id:"deploying-your-app/deploying-code",title:"Deploying to AWS",description:"The Django Starter Project comes with a complete CircleCI configuration,",source:"@site/docs/deploying-your-app/02-deploying-code.md",sourceDirName:"deploying-your-app",slug:"/deploying-your-app/deploying-code",permalink:"/dj-starter/docs/deploying-your-app/deploying-code",draft:!1,editUrl:"https://github.com/shift3/dj-starter/tree/main/packages/create-docusaurus/templates/shared/docs/deploying-your-app/02-deploying-code.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"Provisioning Infrastructure",permalink:"/dj-starter/docs/deploying-your-app/provisioning-infrastructure"},next:{title:"Pagination, Sorting, and Filtering",permalink:"/dj-starter/docs/features/api-pagination-sorting-filtering"}},p={},u=[{value:"Setup CircleCI",id:"setup-circleci",level:2},{value:"Set CircleCI Environment Variables",id:"set-circleci-environment-variables",level:2},{value:"The easy way",id:"the-easy-way",level:3},{value:"The manual way",id:"the-manual-way",level:3},{value:"Deploying to Production",id:"deploying-to-production",level:2}],s={toc:u};function c(e){let{components:t,...n}=e;return(0,r.kt)("wrapper",(0,a.Z)({},s,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"deploying-to-aws"},"Deploying to AWS"),(0,r.kt)("p",null,"The Django Starter Project comes with a complete CircleCI configuration,\nas well as some useful scripts that make deployment a breeze. The\nproject is designed to be deployed automatically via CircleCI."),(0,r.kt)("h2",{id:"setup-circleci"},"Setup CircleCI"),(0,r.kt)("p",null,"Applications are ",(0,r.kt)("strong",{parentName:"p"},"deployed automatically")," by CircleCI when commits are\npushed to ",(0,r.kt)("inlineCode",{parentName:"p"},"develop")," or ",(0,r.kt)("inlineCode",{parentName:"p"},"main"),". Make sure CircleCI is setup on your\nproject by visiting the ",(0,r.kt)("a",{parentName:"p",href:"https://circleci.com/vcs-authorize/"},"CircleCI\ndashboard")," for your project."),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"Commits to the ",(0,r.kt)("inlineCode",{parentName:"li"},"develop"),"  branch are automatically deployed to the\n",(0,r.kt)("strong",{parentName:"li"},"Staging")," environment."),(0,r.kt)("li",{parentName:"ul"},"Commits to the ",(0,r.kt)("inlineCode",{parentName:"li"},"main"),"  branch are automatically deployed to the\n",(0,r.kt)("strong",{parentName:"li"},"Production")," environment.")),(0,r.kt)("h2",{id:"set-circleci-environment-variables"},"Set CircleCI Environment Variables"),(0,r.kt)("p",null,"In order for automatic deploys to work, your CircleCI must be setup with\nthe correct environment variables. "),(0,r.kt)("h3",{id:"the-easy-way"},"The easy way"),(0,r.kt)("p",null,"We include a script that pulls the necessary environment variables from\nyour terraform state, and uploads them to CircleCI for you. In order to\nrun it, you will need to have already provisioned your terraform\ninfrastructure, ",(0,r.kt)("a",{parentName:"p",href:"https://app.circleci.com/projects/project-dashboard/github/Shift3/"},"setup the project on\nCircleCI"),",\nand ",(0,r.kt)("a",{parentName:"p",href:"https://app.circleci.com/settings/user/tokens"},"created a CircleCI API\ntoken"),". Once your have\nretrieved your CircleCI API token, simply run the following command,\nreplacing the values for ",(0,r.kt)("inlineCode",{parentName:"p"},"CIRCLECI_TOKEN")," and ",(0,r.kt)("inlineCode",{parentName:"p"},"PROJECT_NAME")," with your\nown."),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-bash"},"CIRCLECI_TOKEN=my-api-token PROJECT_NAME=my-project scripts/update-circleci.sh\n")),(0,r.kt)("p",null,"Depending on your current ",(0,r.kt)("strong",{parentName:"p"},"terraform workspace")," the script will show\nyou what environment variables you will need, and will ask you if it's\nok to set them on CircleCI. "),(0,r.kt)("p",null,"After the script works, you can make a push to ",(0,r.kt)("inlineCode",{parentName:"p"},"develop")," for staging, or\n",(0,r.kt)("inlineCode",{parentName:"p"},"main")," for production, to start a deploy process and make sure\neverything works."),(0,r.kt)("h3",{id:"the-manual-way"},"The manual way"),(0,r.kt)("p",null,"The following environment variables are required to be set within the\nCircleCI Project Settings. Descriptions (and example values) of the\nenvironment variables follow:"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PROJECT_NAME"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"The name of your project. This variable will be used to tag your docker image file. A safe name would be to use the same name as your git repository. Cannot contain spaces."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"my-project")))),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"STAGING_AWS_ACCESS_KEY_ID"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"The AWS access key ID used to authenticate with AWS."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"AKIAIOSFODNN7EXAMPLE")))),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"STAGING_AWS_SECRET_ACCESS_KEY"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"The AWS secret key used to authenticate with AWS."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")))),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"STAGING_AWS_DEFAULT_REGION"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"The default region your infrastructure is deployed to."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"us-west-2")))),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"STAGING_AWS_ECR_ACCOUNT_URL"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"The ECR (Elastic Container Repository) account url. This will be used to store the docker images that are built for production and staging."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"012345678901.dkr.ecr.us-west-2.amazonaws.com")))),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"STAGING_AWS_ECR_REPO_NAME"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"The ECR repository name, this can be found in the AWS console."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"my-project-ecr-repo")))),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"STAGING_EB_ENVIRONMENT_NAME"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"The EB (Elastic Beanstalk) environment name, this can be found in the AWS console."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"my-project-api-webserver")))),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"STAGING_EB_APPLICATION_NAME"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"The EB application name, this can be found in the AWS console."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"my-project")))),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"STAGING_AWS_ROLE_ARN"),(0,r.kt)("ul",{parentName:"li"},(0,r.kt)("li",{parentName:"ul"},"When using ",(0,r.kt)("a",{parentName:"li",href:"https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html"},"AWS AssumeRole")," (as bitwise does for AWS infastructure in our accounts). You must set this environment variable. When deploying to infrastructure outside of bitwise infrastructure, this variable is optional. The example value is the value you should use on bitwise infrastructure."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"arn:aws:iam::008036621198:role/SuperDevAssumeRole"))))),(0,r.kt)("p",null,"Once all of these are setup, commits to the ",(0,r.kt)("inlineCode",{parentName:"p"},"develop")," branch should automatically deploy to your staging infrastructure. For more details on the deployment process, or if you need to customize it to fit your needs, check out the ",(0,r.kt)("inlineCode",{parentName:"p"},".cirleci/config.yml")," file."),(0,r.kt)("h2",{id:"deploying-to-production"},"Deploying to Production"),(0,r.kt)("p",null,"Production deploys from the ",(0,r.kt)("inlineCode",{parentName:"p"},"main")," branch, and uses the same set of environment variables as staging just with ",(0,r.kt)("inlineCode",{parentName:"p"},"PRODUCTION")," instead of ",(0,r.kt)("inlineCode",{parentName:"p"},"STAGING")," in the names. The list of those variables follow:"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PRODUCTION_AWS_ACCESS_KEY_ID")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PRODUCTION_AWS_SECRET_ACCESS_KEY")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PRODUCTION_AWS_DEFAULT_REGION")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PRODUCTION_AWS_ECR_ACCOUNT_URL")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PRODUCTION_AWS_ECR_REPO_NAME")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PRODUCTION_EB_ENVIRONMENT_NAME")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PRODUCTION_EB_APPLICATION_NAME")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"PRODUCTION_AWS_ROLE_ARN")," (optional)")))}c.isMDXComponent=!0}}]);