# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (172)

```
 10443  GET              /                                                dashboard
 14314  GET              /api/abo/status                                  api_abo_status
 10516  GET              /api/active-recordings                           api_active_recordings
 14385  GET              /api/activity-pulse                              api_activity_pulse
 14192  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 21070  GET/POST         /api/audio/config                                api_audio_config
 21100  POST             /api/audio/testtone                              api_audio_testtone
 14258  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14282  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14286  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11970  GET              /api/automation/status                           api_automation_status
 11992  POST             /api/automation/toggle                           api_automation_toggle
 13189  GET              /api/azrael/agents                               api_azrael_agents
 11862  POST             /api/azrael/ask                                  api_azrael_ask
 21306  GET/POST         /api/azrael/context                              api_azrael_context
 12894  GET              /api/azrael/core                                 api_azrael_core
 21440  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21430  GET              /api/azrael/live_status                          api_azrael_live_status
 21448  POST             /api/azrael/live_test                            api_azrael_live_test
 13198  GET              /api/azrael/memories                             api_azrael_memories
 21496  POST             /api/azrael/persona                              api_azrael_persona_set
 21487  GET              /api/azrael/personas                             api_azrael_personas
 21524  GET              /api/azrael/piper_status                         api_azrael_piper_status
 21279  POST             /api/azrael/react                                api_azrael_react
 21315  GET              /api/azrael/reaction                             api_azrael_reaction
 21467  GET              /api/azrael/reactions                            api_azrael_reactions
 21517  GET              /api/azrael/transcript                           api_azrael_transcript
 21402  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21377  GET              /api/azrael/voices                               api_azrael_voices
 21541  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10815  GET              /api/backoff-watch                               api_backoff_watch
 13673  POST             /api/backup/run                                  api_backup_run
 13639  GET              /api/backup/status                               api_backup_status
 13628  POST             /api/backup/system                               api_backup_system
 14224  GET              /api/bandwidth/live                              api_bandwidth_live
 14177  GET              /api/bookmarks                                   api_bookmarks_list
 11078  GET              /api/brain                                       api_brain
 11015  GET              /api/brain/alarms                                api_brain_alarms
 11000  GET              /api/brain/creator                               api_brain_creator
 10977  GET              /api/brain/graph                                 api_brain_graph
 11038  GET              /api/brain/growth                                api_brain_growth
  9993  GET              /api/brain/health                                api_brain_health
 22022  GET              /api/channel/categories                          api_channel_categories
 22028  POST             /api/channel/set                                 api_channel_set
 21838  GET              /api/channels/status                             api_channels_status
 20714  POST             /api/chat/send                                   api_chat_send
 13393  GET              /api/chat/send_status                            api_chat_send_status
 10497  GET              /api/checks                                      api_checks
 21343  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21326  GET              /api/clips                                       api_clips
 21359  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20992  GET              /api/cohost                                      api_cohost
 21004  POST             /api/cohost/config                               api_cohost_config
 14693  GET              /api/community/stats                             api_community_stats
 22662  GET              /api/data/export                                 api_data_export
 20918  GET              /api/debug/threads                               api_debug_threads
 23489  GET              /api/defense/attacks                             api_defense_attacks
 23456  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23474  GET              /api/defense/fail2ban                            api_defense_fail2ban
 23180  GET              /api/defense/overview                            api_defense_overview
 13735  POST             /api/discord/announce                            api_discord_announce
 13463  GET              /api/discord/clips_week                          api_discord_clips_week
 13679  GET              /api/discord/community                           api_discord_community
 13421  GET              /api/discord/invite                              api_discord_invite
 12995  GET              /api/discord/overview                            api_discord_overview
 13081  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14206  GET              /api/events                                      api_events
 13510  GET              /api/events/stream                               api_events_stream
 14219  GET              /api/forecast/storage                            api_forecast_storage
 12008  GET              /api/freeai/status                               api_freeai_status
 12937  GET              /api/health                                      api_health
 14237  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14233  GET              /api/heatmap/recordings                          api_heatmap_recordings
 21041  GET              /api/highlights                                  api_highlights
 21053  POST             /api/highlights/config                           api_highlights_config
 21879  GET              /api/kick/channel                                api_kick_channel
 21900  POST             /api/kick/channel                                api_kick_channel_set
 12694  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 12762  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 12740  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 12679  GET              /api/kick/oauth/start                            api_kick_oauth_start
 12719  GET              /api/kick/oauth/status                           api_kick_oauth_status
 21118  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 21187  POST             /api/kickmod/config                              api_kickmod_config
 21232  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 21246  GET              /api/kickmod/learned                             api_kickmod_learned
 21273  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 21253  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21584  POST             /api/kickmod/say                                 api_kickmod_say
 21560  POST             /api/kickmod/start                               api_kickmod_start
 21158  GET              /api/kickmod/status                              api_kickmod_status
 21571  POST             /api/kickmod/stop                                api_kickmod_stop
 10377  POST             /api/login                                       dashboard_login_submit
 14678  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14647  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13358  GET              /api/notify/status                               api_notify_status
 13369  POST             /api/notify/test                                 api_notify_test
 10601  GET              /api/outcomes                                    api_outcomes
 22499  POST             /api/overlay/config                              api_overlay_config
 22486  POST             /api/overlay/event                               api_overlay_event
 22391  GET              /api/overlay/state                               api_overlay_state
 10634  GET              /api/profile/<username>                          api_profile
 14403  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14245  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14368  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14345  GET              /api/proxy/trend                                 api_proxy_trend
 12463  GET              /api/public/stats                                api_public_stats
 10477  GET              /api/pulse                                       api_pulse
 13813  GET              /api/recording-attempts                          api_recording_attempts
 20649  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20627  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20668  POST             /api/restream/<int:rid>/start                    api_restream_start
 20939  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22353  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20603  POST             /api/restream/create                             api_restream_create
 12770  GET              /api/restream/deck                               api_restream_deck
 11944  GET              /api/restream/health                             api_restream_health
 22375  POST             /api/restream/layout                             api_restream_layout
 20576  GET              /api/restream/list                               api_restream_list
 11913  POST             /api/restream/report                             api_restream_report
 20952  POST             /api/restream/start_all                          api_restream_start_all
 20978  POST             /api/restream/stop_all                           api_restream_stop_all
 12119  GET              /api/restream/testpush                           api_testpush_status
 12144  POST             /api/restream/testpush                           api_testpush_run
 14778  GET              /api/restream/verify                             api_restream_verify
 13441  GET              /api/retention/preview                           api_retention_preview
 13450  POST             /api/retention/run                               api_retention_run
 14162  GET              /api/search                                      api_search
 23227  GET              /api/selftest                                    api_selftest
 20685  GET              /api/shield/stats                                api_shield_stats
 10538  GET              /api/storage                                     api_storage
 10545  POST             /api/storage/cleanup                             api_storage_cleanup
 14299  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11883  GET              /api/stream/timeline                             api_stream_timeline
 13069  GET              /api/stream/transcript                           api_stream_transcript
 10569  GET              /api/summary/preview                             api_summary_preview
 13878  GET              /api/system                                      api_system
 14726  GET              /api/system/check_timing                         api_check_timing
 15049  GET              /api/system/config_drift                         api_config_drift
 13105  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13216  GET              /api/system/preflight                            api_system_preflight
 13342  GET              /api/system/preflight_history                    api_system_preflight_history
 13575  GET              /api/system/resilience                           api_system_resilience
 14197  GET              /api/tags                                        api_tags_list
 10511  GET              /api/top                                         api_top
 10870  GET              /api/trend-7d                                    api_trend_7d
 21391  GET              /api/tts/<fn>                                    api_tts_file
 15021  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 14973  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 14997  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 14951  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 22527  GET              /api/upload_window                               api_upload_window
 10615  GET              /api/userstats                                   api_userstats
 12511  GET              /api/version                                     api_version
 14872  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 14893  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 14905  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 14830  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 14854  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 14808  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 26917  GET              /api/youtube/sendrate                            api_youtube_sendrate
 13851  GET              /archive/<int:eid>/download                      archive_download
 13908  GET              /download/<int:recording_id>                     download
 13791  GET              /health                                          health
 20887  GET              /healthz                                         healthz
 10368  GET              /login                                           dashboard_login_page
 10398  GET              /logout                                          dashboard_logout
 10405  GET              /manifest.webmanifest                            pwa_manifest
 13133  GET              /metrics                                         api_prometheus_metrics
 22336  GET              /overlay                                         overlay_page
 10429  GET              /pwa-icon-<variant>.png                          pwa_icon
 10415  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (187)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    57  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    46  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   204  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    70  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 23932  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 24391  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 24023  /assign_role            Rolle/Gruppe einem Mitglied geben
 24069  /ban                    Mitglied bannen
 24723  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 24647  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 24687  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 24672  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 24514  /clips                  Letzte Highlight-Clips eines Users
 23984  /create_category        Kategorie anlegen
 23953  /create_channel         Text-Channel anlegen (optional in Kategorie)
 24012  /create_group           Nutzergruppe (= Rolle) anlegen
 23995  /create_role            Rolle / Nutzergruppe anlegen
 23969  /create_voice           Voice-Channel anlegen
 24305  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 24421  /event                  Community-Event ankündigen (Admin) — mit Countdown
 24464  /events                 Kommende Community-Events anzeigen
 24560  /follow                 Bei Live-Gang eines Streamers gepingt werden
 24544  /help                   Alle Bot-Befehle anzeigen
 24058  /kick                   Mitglied kicken
 24287  /leaderboard            Top-10 der Community nach XP
 24500  /livenow                Welche getrackten User sind gerade live
 24530  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 24361  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 24093  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 24273  /rank                   Dein Level und Rang anzeigen
 24487  /recstatus              Aktuell laufende Aufnahmen
 24034  /remove_role            Rolle/Gruppe entfernen
 23946  /restream_status        Restream-Status
 24045  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 24238  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 24256  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 24586  /stats                  Statistik zu einem getrackten Streamer
 23858  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 24882  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 24779  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 24755  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 24080  /timeout                Mitglied stummschalten (Minuten)
 24658  /topstreamers           Rangliste der Streamer nach Aufnahmen
 23888  /track                  TikTok-User tracken
 23872  /tracklist              Getrackte TikTok-User dieses Servers
 24575  /unfollow               Live-Pings für einen Streamer abbestellen
 23921  /untrack                TikTok-User nicht mehr tracken
 24608  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 24632  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 25366  on_member_join
 25328  on_message
 24969  on_raw_reaction_add
 25401  on_ready
```

## Top-Level-Symbole in bot.py (519 Funktionen, 2 Klassen)

```
  2488-2489   _abo_key
  2509-2527   _abo_probe_dump
 22769-22779  _active_recorder_sync
 17870-17877  _ad_allowlist
 18992-18998  _agent_for
 22781-22799  _ai_calls_total_sync
 19001-19017  _ai_telemetry
 19499-19517  _alert
 25517-25567  _alert_monitor_loop
 25948-26010  _announce_loop
  3430-3433   _anthropic_key
  3440-3442   _anthropic_model
 10121-10124  _arg_int
  2480-2485   _as_dict
 15730-15735  _audio_cfg
 19653-19675  _audio_tap_cmd
 10289-10300  _auth_cookie
 10256-10285  _auth_guard
  1636-1641   _auto_on
 20552-20570  _auto_restream_loop
 27078-27093  _azrael_broadcast_reply
 26978-27000  _azrael_chat_reply
 26961-26975  _azrael_chat_should_reply
 27006-27008  _azrael_gate_cfg
 19022-19036  _azrael_live_state
 22239-22253  _azrael_overlay_state
 19382-19436  _azrael_proactive_loop
 18841-18897  _azrael_reaction_to_chats
 27011-27018  _azrael_reply_all_chats
 26948-26958  _azrael_self_names
 27046-27075  _azrael_send_to
 19039-19060  _azrael_system
 25686-25689  _backup_active
 25767-25780  _backup_loop
 17758-17759  _badwords_path
 25479-25488  _brain_growth_loop
 10946-10973  _brain_growth_snapshot
  2416-2436   _brain_hint_delay
 10938-10940  _brain_history_for
  6509-6537   _brain_notify
 10915-10936  _brain_record
 10942-10944  _brain_stream_recent
 13489-13506  _browser_push
  6553-6640   _build_daily_summary
  2919-3099   _build_native_cmd
 16078-16265  _build_restream_cmd
  3143-3176   _build_ytdlp_cmd
 22721-22728  _cached_probe
  5331-5358   _can_stop_tracking
  1816-1838   _capture_set_cookies
 14462-14465  _cfg_get
 14468-14470  _cfg_set
 21983-22018  _channel_set_all
 15328-15331  _chat_connected
 15334-15350  _chat_disconnected
  8601-8612   _chat_is_forum
 15370-15372  _chat_sanitize
 15374-15383  _chat_src_ok
 15313-15325  _chat_stat
 15353-15356  _chat_stats_snapshot
  3705-3716   _check_ai_alive_sync
  3719-3731   _check_ai_models_sync
 22730-22743  _check_redis_alive_sync
 22745-22765  _check_redis_version_sync
 11545-11588  _classify_pool_anonymity
 11591-11608  _classify_pool_anonymity_bg
   794-798    _claude_chat_sync_metered
 10150-10157  _client_ip
 26042-26069  _clip_prune
 26072-26082  _clip_recfile_for
 26598-26604  _clip_should_velocity
 26123-26205  _clip_to_discord
  3603-3612   _close_ai_session
 27122-27137  _cohost_broadcast
 27104-27108  _cohost_cfg
 27163-27175  _cohost_fire_highlight
 27111-27119  _cohost_gate
 27140-27160  _cohost_highlight
 26254-26288  _community_events_loop
 10769-10771  _conv_messages
  6942-6985   _cookie_alarm_loop
  1888-1892   _cookie_autorefresh_info
  1793-1797   _cookie_header
 13539-13571  _cpu_load_snapshot
  3913-3925   _create_index_safe
 22982-23088  _crowdsec_status
 22948-22979  _crowdsec_via_lapi
 22813-22831  _cscli_bin
 22837-22850  _cscli_path
  6832-6857   _daily_summary_loop
 22868-22885  _darf_journal_lesen
 25491-25514  _db_maintenance_loop
  6801-6829   _db_vacuum_loop
 17893-17917  _detect_foreign_ad
  1374-1385   _diag_path_owner
 19288-19332  _director_finalize
 20099-20106  _director_for
 19237-19285  _director_mark
 26492-26527  _disc_automod_check
 26465-26471  _disc_state_get
 26474-26481  _disc_state_set
 23531-23544  _discord_guild_filesize_bytes
 23730-23739  _discord_invite
 26426-26462  _discord_live_thread
 19439-19451  _discord_notify
 23631-23656  _discord_ops_alert
 26324-26422  _discord_post_user
 23795-25476  _discord_run_once
 23669-23727  _discord_start
 26013-26019  _discord_stop
 23552-23554  _discord_upload_limit_label
 23547-23549  _discord_upload_limit_mb
  6860-6937   _disk_alarm_loop
 28524-28573  _disk_autoclean
 28576-28589  _disk_guard_loop
 28516-28521  _disk_pct
 15687-15689  _drawtext_chain
 14005-14007  _dump_all_threads
 11470-11534  _enrich_proxies_with_geo
  2033-2077   _ensure_cookie_file_netscape
 23742-23792  _ensure_discord_invite
 26219-26251  _ensure_error_channel
  8660-8663   _ensure_notify_topic
 11715-11752  _ensure_proxy_ready
  8614-8641   _ensure_topic
   652-654    _env_int
   657-659    _env_int_range
 26291-26321  _error_channel_loop
 19483-19496  _event_webhook
 15136-15149  _evolution_loop
  5951-5985   _extract_file_payload
  2165-2167   _extract_urls_from_streamurl_node
 22853-22860  _f2b_sudo_hint
 19519-19521  _faster_whisper_available
 17782-17794  _fetch_ldnoobw_de
 11359-11377  _fetch_proxy_list
 19933-19961  _fetch_tiktok_room_id
   728-731    _ff_cmd
 15850-15855  _find_chromium
  3136-3140   _find_external_recorder
  2170-2172   _find_stream_urls
 14513-14538  _fire_webhooks
  7721-7730   _fork_safe
   809-818    _freeai_chat_sync_metered
 22903-22945  _geo_lookup_ips
  3592-3601   _get_ai_session
  7555-7595   _get_live_info
  2706-2713   _get_resolve_semaphore
  7956-8322   _handle_single_tracking
 28368-28370  _hb
 28373-28390  _hb_while
 15388-15390  _highlight_cfg
 15393-15422  _highlight_observe
 15858-15863  _htmlov_screenshot_cmd
 19677-19687  _httpx_proxy
 14546-14558  _in_quiet_hours
 29403-29434  _install_fast_eventloop
 10016-10070  _install_fast_json
 14010-14026  _install_faulthandler
 20795-20804  _intel_ensure_schema
 20842-20877  _intel_index_loop
 20816-20826  _intel_index_one
 20807-20813  _intel_semantic
  5320-5329   _is_authorized
  7886-7892   _is_dead
  2155-2157   _is_hevc
 22888-22894  _is_private_ip
  1538-1545   _is_process_running
  6539-6550   _is_quiet_hours
  1175-1184   _is_upload_window
 10105-10118  _json_error_handler
  6759-6789   _kick_broadcaster_id
 12045-12064  _kick_channel_live
  6673-6715   _kick_follower_count
 12657-12670  _kick_oauth_exchange
 12673-12675  _kick_oauth_page
 12616-12620  _kick_redirect_public
 12611-12613  _kick_redirect_source
 12603-12608  _kick_redirect_uri
  6658-6660   _kick_slug
 12623-12654  _kick_user_token
  3962-3965   _kind_from_filename
 14575-14580  _latest_popularity
 17804-17810  _learned_load
 17801-17802  _learned_path
 17812-17820  _learned_save
 20314-20347  _live_react_loop
 20110-20303  _live_react_worker
 18900-18911  _live_transcript_push
 20305-20312  _live_users
 19335-19379  _living_title_loop
 17761-17769  _load_banned_words_file
  1714-1787   _load_cookies_dict
 25692-25764  _local_backup_scan
 10087-10101  _log_5xx
 16273-16285  _looks_like_codec_err
 16268-16270  _looks_like_source_expired
  7802-7832   _loop_fehler
 14030-14039  _loop_heartbeat
 28338-28365  _loop_lag_monitor
 14042-14110  _loop_watchdog_thread
 18780-18794  _loyalty_add
 18771-18777  _loyalty_get
 18797-18805  _loyalty_top
 14712-14714  _manual_donations_total
  7894-7895   _mark_dead
 12216-12232  _marketing_loop
 27025-27043  _maybe_handle_command
 28675-28699  _maybe_hype_clip
  3880-3903   _migrate_columns
 27302-27313  _mod_is_exempt
 27316-27321  _mod_warn_first
 27324-27327  _mod_warn_text
 15176-15184  _modlog
   928-930    _multistream_targets
  7733-7734   _nc_create_subprocess_exec
  7737-7738   _nc_create_subprocess_shell
 12468-12485  _news_loop
 15214-15216  _normalize_ingest
  2347-2364   _note_check_duration
  8654-8657   _notify_topic_name
 12567-12578  _oauth_redirect_env
 12594-12600  _oauth_redirect_source
 12581-12591  _oauth_redirect_uri
 18926-18934  _oracle_memories
 19192-19226  _oracle_memorize
 18937-18950  _oracle_persona
 18919-18923  _oracle_recent_text
 15513-15521  _ov_atomic_write
 15501-15507  _ov_bar
 17717-17729  _ov_clip_text
 15510-15511  _ov_oneline
 22303-22332  _overlay_push
 15804-15847  _overlay_render_size
 15275-15279  _overlay_session_reset
 22255-22258  _overlay_src_ok
 17880-17890  _own_invites
 15799-15801  _parse_size
 23096-23176  _parse_ssh_attacks
  7157-7190   _pause_resume_cmd
  1842-1886   _persist_refreshed_cookies
  1680-1712   _pick_checked_pull_proxy
 10186-10199  _pin_auth_value
 10245-10246  _pin_clear_fail
 10225-10228  _pin_locked
 10231-10242  _pin_note_fail
 10202-10222  _pin_ok
 22145-22147  _piper_available
 22110-22132  _piper_list_voices
 22152-22177  _piper_pick_model
 22189-22236  _piper_say
 22103-22107  _piper_voice_roots
 14475-14510  _post_json_threaded
 15778-15796  _probe_video_size
  1566-1583   _proc_is_recorder
 11457-11468  _proxy_geo_cache_put
 11684-11712  _proxy_pool_refresh_loop
  1646-1677   _proxy_report_recording
 13995-13997  _prune_stall_dumps
 12526-12564  _public_base_url
 12286-12407  _public_stats
 19454-19480  _push_notify
 10347-10349  _pwa_dir
 11428-11443  _quick_validate_proxy
 14541-14543  _quiet_hours_config
 10312-10345  _rate_guard
 18745-18751  _react_warn
  7641-7680   _reap_proc
  2387-2409   _record_check_outcome
   723-725    _redact_stream_urls
 11611-11681  _refresh_proxy_pool
 22135-22141  _resolve_piper_model
  2181-2271   _resolve_via_html
  2529-2683   _resolve_via_webcast_api_v2
  2746-2808   _resolve_via_ytdlp
 26644-26773  _resolve_youtube_ingest
 20386-20393  _restream_active_platforms
 15260-15271  _restream_active_sources
 19964-20063  _restream_chat_guardian
 15425-15497  _restream_chat_push
 15187-15199  _restream_enabled
 15866-15953  _restream_html_overlay_start
 15956-15969  _restream_html_overlay_stop
  1123-1125   _restream_layout_mode
 15225-15248  _restream_overlay_files
 20351-20383  _restream_platform_state
 20514-20549  _restream_resume_after_restart
 16017-16075  _restream_tts_enqueue_wav
 15740-15772  _restream_tts_feeder
 15737-15738  _restream_tts_fifo_path
 15972-15999  _restream_tts_start
 16001-16015  _restream_tts_stop
 20396-20511  _restream_verify_loop
 25657-25669  _retention_loop
 25616-25654  _retention_scan
  2491-2493   _room_is_abo
  5989-6106   _run_ai_call
 14133-14146  _run_async_from_flask
 22897-22900  _run_priv
 29391-29399  _run_selfcheck_and_exit
 25672-25683  _s3_client
  7897-7943   _safe_send
  4584-4600   _sample_net_throughput
 17771-17779  _save_banned_words_file
  2439-2466   _schedule_next_check
 25570-25613  _scheduler_loop
  3906-3910   _schema_pk
 14150-14155  _scraper_session
 27330-27369  _screen_full
 12953-12990  _sec_headers
  2160-2162   _select_stream_from_data_section
 29204-29388  _selfcheck
  8666-8700   _send_live_notice
  1198-1202   _should_defer_upload
 26085-26120  _shrink_for_discord
 10352-10364  _sicheres_ziel
 28596-28613  _sign_health_check
 28616-28635  _sign_health_loop
  7750-7761   _spawn
  7764-7794   _spawn_from_flask
 23220-23223  _st_befund
 19689-19930  _start_chat_listener
 14113-14130  _start_loop_watchdog
 12431-12459  _stats_loop
 12410-12413  _stats_output_path
 12416-12428  _stats_write
  8394-8410   _storage_cleanup_loop
 28655-28662  _story_for
  3198-3204   _stream_url_expiry
  3213-3219   _stream_url_is_fresh
  3206-3211   _stream_url_ttl
 17844-17851  _streamer_persona_get
 17826-17832  _streamer_personas_load
 17823-17824  _streamer_personas_path
 17834-17842  _streamer_personas_save
 15692-15696  _studio_chain
 25789-25911  _system_backup
 25914-25944  _system_backup_loop
 11380-11419  _test_proxy
 12086-12095  _testpush_cfg
 12098-12115  _testpush_exec
 12067-12083  _testpush_resolve_live
  8573-8583   _tg_topics_load_into_mem
  8570-8571   _tg_topics_path
  8585-8592   _tg_topics_save
 10160-10168  _token_ok
  8595-8599   _topic_forget
 14561-14572  _tracking_max_duration
  4171-4185   _tracking_remove_cleanup
  4202-4214   _tracking_resume_cleanup
  1432-1455   _try_attach_file_handler
 22179-22187  _tts_cleanup
 12023-12027  _tunnel_effective
 21605-21658  _twitch_channel_status
 27372-27515  _twitch_chat_loop
 27186-27289  _twitch_eventsub_loop
 15042-15045  _twitch_oauth_page
  1221-1234   _upload_queue_add
  1245-1247   _upload_queue_count
  1204-1213   _upload_queue_load
  1194-1196   _upload_queue_path
  1236-1243   _upload_queue_remove
  1215-1219   _upload_queue_save
  1249-1290   _upload_window_loop
  7614-7621   _uptime_s
 15202-15211  _url_host
   703-720    _url_ohne_zugang
   787-791    _usage_record_claude
  7835-7879   _verbindung_verloren
  6718-6749   _viewer_sample_loop
  6791-6798   _viewer_stats
 10249-10252  _wants_html
  7624-7638   _warn_empty_env
 28411-28506  _watchdog_loop
 26927-26935  _wchat_thank_ok
 19523-19553  _whisper_get_model
  7711-7718   _whisper_native_section
 18732-18738  _whisper_pool
 19622-19651  _whisper_segments
 19555-19619  _whisper_transcribe
 15523-15685  _write_restream_overlay
 27543-27622  _youtube_api_chat_loop
 21661-21764  _youtube_api_status
 21767-21834  _youtube_channel_status
 27625-27785  _youtube_chat_loop
 26779-26792  _youtube_restream_autoconfig
 26795-26819  _youtube_restream_autoconfig_inner
 26885-26913  _youtube_send
 21939-21980  _youtube_set_channel
 26822-26856  _yt_access_token
 26859-26874  _yt_live_chat_id
 27536-27540  _yt_oauth_configured
 26880-26882  _yt_sendrate_cfg
 27518-27533  _yt_timeout
  2730-2731   _ytdlp_detect_available
  2733-2744   _ytdlp_note_result
 14000-14002  _zombie_child_count
  7491-7515   about
  4081-4085   add_ai_log_entry
  3998-4001   add_archive_entry
  4697-4712   add_archive_rule
  4373-4407   add_recording
  4146-4163   add_tracking
  6109-6142   ai
  3745-3784   ai_chat
  3818-3828   ai_history_append
  3830-3835   ai_history_clear
  3807-3816   ai_history_load
  3792-3805   ai_rate_limit_check
  6171-6179   aireset
 19063-19082  azrael_chat
 27790-27912  brain_cmd
  3222-3406   build_recording_cmd
  4166-4169   bulk_add_trackings
  6988-7047   bulkadd
  8413-8553   check_all_trackings
  4218-4230   claim_live_transition
 17920-18675  class KickModerator
 16288-17604  class RestreamManager
 11797-11839  classify_proxy_anonymity
  6217-6415   cleanup
  5180-5221   cleanup_old_recordings
  4364-4371   clear_recording
 26530-26595  clip_moment
  4528-4577   compute_storage_forecast
  7110-7154   cookies_cmd
  4137-4143   count_trackings_for_chat
  4068-4079   decide_preferred_recorder
  4008-4011   delete_archive_entry
  4714-4722   delete_archive_rule
  5646-5793   diag
 28024-28085  einnahmen_cmd
  4522-4525   find_recordings_by_fingerprint
  4029-4045   finish_recording_attempt
  4190-4192   get_all_active_trackings
  4096-4099   get_all_checks
  4409-4412   get_all_recordings
  4471-4473   get_all_tags_with_counts
  4499-4502   get_annotations_for_recording
  4003-4006   get_archive_entry
  4492-4495   get_bookmarked_recordings
  1909-2026   get_cookie_health
  4459-4465   get_event_log
  4052-4066   get_last_recording_attempt
  2811-2916   get_live_status
  4980-4983   get_manual_recordings
  4507-4510   get_or_compute_inspect_sync
  5256-5300   get_outcome_breakdown
  4478-4481   get_priority_poll_interval
  4675-4684   get_profile_snapshots
  4047-4050   get_recent_recording_attempts
  4414-4417   get_recording_by_id
  4485-4488   get_recording_note
  3540-3563   get_redis
  4126-4129   get_stats
  5147-5178   get_storage_stats
  4815-4817   get_tiktok_status_distribution
  4232-4241   get_tracking_state
  4187-4188   get_trackings_for_group
  4996-4999   get_trash_recordings
  9321-9984   handle_recording_finished
  3928-3953   init_db
  5070-5124   inspect_stream_url
 22298-22300  is_revenue_platform
  4687-4695   list_archive_rules
  5450-5488   live
  7946-7954   live_check_worker
  3615-3649   llm_chat
  3672-3700   llm_chat_sync
  3657-3669   llm_list_models
  4425-4451   log_event
  1500-1533   log_recording_failure
  7304-7353   logs_cmd
 28703-29194  main
  6145-6168   on_ai_media
  7430-7456   on_ai_reply
  7459-7488   on_azrael_mention
  7520-7550   on_callback
 19085-19189  oracle_handle
  7193-7196   pause_tracking
  5310-5315   profile_keyboard
  7255-7301   quota
  8324-8391   reaper_loop
  4811-4813   record_tiktok_status
  6184-6214   recstatus
  3565-3573   redis_get_json
  3575-3581   redis_set_json
 28088-28098  report_cmd
 11842-11844  report_proxy_result
  2274-2301   resolve_tiktok_live_stream
  4991-4994   restore_recording
  7199-7202   resume_tracking
  4725-4805   run_archive_rules
 28101-28318  run_bot
 13922-13969  run_flask
  4603-4648   sample_bandwidth_for_active
  4654-4673   save_profile_snapshot
  4088-4094   save_tiktok_check
  4356-4362   set_recording_file
  4195-4199   set_tracking_paused
  4986-4989   soft_delete_recording
  8706-9319   split_and_send_video
  5363-5405   start
  4013-4027   start_recording_attempt
  6418-6456   stats
  4961-4978   stop_manual_recording
  7205-7252   stoprec
  6643-6651   summary_cmd
  7356-7427   sysres
  5795-5939   teststream
  5407-5448   tiktok
  7050-7107   topusers
  5525-5582   track
  5490-5522   track_exact
  5596-5644   tracklist
  4827-4959   trigger_manual_recording
  4317-4354   try_acquire_recording_lock
  5002-5061   universal_search
  5584-5594   untrack
 27915-28021  update_cmd
  4517-4520   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
i18n.py                aus_accept_language, configure, katalog, normalisieren, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
