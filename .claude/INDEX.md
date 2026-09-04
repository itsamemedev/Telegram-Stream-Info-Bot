# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (35)

```
 10012  GET              /                                                dashboard
 11928  GET              /api/abo/status                                  api_abo_status
 11882  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10800  GET              /api/automation/status                           api_automation_status
 10822  POST             /api/automation/toggle                           api_automation_toggle
 18666  GET              /api/channel/categories                          api_channel_categories
 18672  POST             /api/channel/set                                 api_channel_set
 18519  GET              /api/channels/status                             api_channels_status
 18193  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18176  GET              /api/clips                                       api_clips
 18222  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18101  GET              /api/debug/threads                               api_debug_threads
 11893  GET              /api/events                                      api_events
 11465  GET              /api/events/stream                               api_events_stream
 11292  GET              /api/health                                      api_health
 18135  POST             /api/highlights/config                           api_highlights_config
  9946  POST             /api/login                                       dashboard_login_submit
 12221  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11380  GET              /api/notify/status                               api_notify_status
 11391  POST             /api/notify/test                                 api_notify_test
 11982  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11959  GET              /api/proxy/trend                                 api_proxy_trend
 19522  GET              /api/selftest                                    api_selftest
 18242  GET              /api/tts/<fn>                                    api_tts_file
 18968  GET              /api/upload_window                               api_upload_window
 11582  GET              /archive/<int:eid>/download                      archive_download
 11610  GET              /download/<int:recording_id>                     download
 11539  GET              /health                                          health
 18070  GET              /healthz                                         healthz
  9937  GET              /login                                           dashboard_login_page
  9967  GET              /logout                                          dashboard_logout
  9974  GET              /manifest.webmanifest                            pwa_manifest
 18941  GET              /overlay                                         overlay_page
  9998  GET              /pwa-icon-<variant>.png                          pwa_icon
  9984  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (325)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   394  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1003  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   743  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   874  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   854  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   892  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   816  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   551  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   649  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1241  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1273  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   340  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   956  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   936  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1109  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1157  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1208  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1067  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   911  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   389  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   653  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   535  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   518  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   510  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   346  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   362  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   697  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   662  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   682  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   569  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   371  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   348  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   161  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   415  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   284  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   269  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   192  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    70  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    77  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   469  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   213  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   240  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   200  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   366  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   386  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   381  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   457  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   220  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   400  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   267  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   334  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   362  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   213  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   280  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   515  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   178  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   161  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   401  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   225  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   142  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   832  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   914  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   942  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   953  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   819  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   881  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   868  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   849  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   319  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   494  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   489  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   537  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   420  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   747  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   511  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   474  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   447  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   721  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   591  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   680  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   586  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   519  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   299  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   764  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   387  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   642  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   797  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   782  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   343  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   581  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   567  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   550  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   607  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   700  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   596  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   325  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   315  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   350  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   338  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
   428  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   206  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    72  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   370  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   361  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   176  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   252  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   463  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   429  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   488  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   468  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   451  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   444  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   238  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 20192  /ai                     
 20665  /ask                    
 20283  /assign_role            
 20329  /ban                    
 20997  /botstats               
 20921  /clearwarns             
 20961  /clip                   
 20946  /clipoftheweek          
 20788  /clips                  
 20244  /create_category        
 20213  /create_channel         
 20272  /create_group           
 20255  /create_role            
 20229  /create_voice           
 20565  /daily                  
 20695  /event                  
 20738  /events                 
 20834  /follow                 
 20818  /help                   
 20318  /kick                   
 20547  /leaderboard            
 20774  /livenow                
 20804  /post_test              
 20635  /profile                
 20353  /purge                  
 20533  /rank                   
 20761  /recstatus              
 20294  /remove_role            
 20206  /restream_status        
 20305  /set_channel_perms      
 20498  /setup_community        
 20516  /setup_targets          
 20860  /stats                  
 20118  /status                 
 21156  /streaminfo             
 21053  /sys_report             
 21029  /sys_unpause            
 20340  /timeout                
 20932  /topstreamers           
 20148  /track                  
 20132  /tracklist              
 20849  /unfollow               
 20181  /untrack                
 20882  /warn                   
 20906  /warnings               
```

## Discord-Events (4)

```
 21654  on_member_join
 21616  on_message
 21243  on_raw_reaction_add
 21689  on_ready
```

## Top-Level-Symbole in bot.py (469 Funktionen, 2 Klassen)

```
  2477-2478   _abo_key
  2498-2516   _abo_probe_dump
 15231-15238  _ad_allowlist
 16372-16378  _agent_for
 16381-16397  _ai_telemetry
 16886-16904  _alert
 21828-21878  _alert_monitor_loop
 22230-22292  _announce_loop
  3419-3422   _anthropic_key
  3429-3431   _anthropic_model
  9690-9693   _arg_int
  2469-2474   _as_dict
 17039-17061  _audio_tap_cmd
  9858-9869   _auth_cookie
  9825-9854   _auth_guard
  1707-1712   _auto_on
 17932-17950  _auto_restream_loop
 23371-23386  _azrael_broadcast_reply
 23271-23293  _azrael_chat_reply
 23254-23268  _azrael_chat_should_reply
 23299-23301  _azrael_gate_cfg
 16402-16416  _azrael_live_state
 18853-18867  _azrael_overlay_state
 16768-16822  _azrael_proactive_loop
 16220-16276  _azrael_reaction_to_chats
 23304-23311  _azrael_reply_all_chats
 23241-23251  _azrael_self_names
 23339-23368  _azrael_send_to
 16422-16443  _azrael_system
 21962-21965  _backup_active
 22043-22056  _backup_loop
 21767-21776  _brain_growth_loop
 10191-10218  _brain_growth_snapshot
  2405-2425   _brain_hint_delay
  6097-6125   _brain_notify
 11444-11461  _browser_push
  6141-6228   _build_daily_summary
  2908-3088   _build_native_cmd
 13417-13604  _build_restream_cmd
  3132-3165   _build_ytdlp_cmd
  4919-4946   _can_stop_tracking
  1820-1842   _capture_set_cookies
 12036-12039  _cfg_get
 12042-12044  _cfg_set
 18627-18662  _channel_set_all
 12575-12578  _chat_connected
 12581-12597  _chat_disconnected
  8176-8187   _chat_is_forum
 12617-12619  _chat_sanitize
 12560-12572  _chat_stat
 12600-12603  _chat_stats_snapshot
  3702-3714   _check_ai_models_sync
 10473-10516  _classify_pool_anonymity
 10519-10536  _classify_pool_anonymity_bg
   814-836    _claude_chat_sync_metered
  9719-9726   _client_ip
 22324-22351  _clip_prune
 22354-22364  _clip_recfile_for
 22905-22911  _clip_should_velocity
 22405-22487  _clip_to_discord
  3595-3604   _close_ai_session
 23417-23432  _cohost_broadcast
 23402-23403  _cohost_cfg
 23458-23470  _cohost_fire_highlight
 23406-23414  _cohost_gate
 23435-23455  _cohost_highlight
 22536-22598  _community_events_loop
 10121-10123  _conv_messages
  6500-6543   _cookie_alarm_loop
  1892-1896   _cookie_autorefresh_info
  1797-1801   _cookie_header
  3908-3920   _create_index_safe
 19300-19406  _crowdsec_status
 19246-19297  _crowdsec_via_lapi
 19150-19168  _cscli_bin
 19177-19190  _cscli_path
  6390-6415   _daily_summary_loop
 19208-19225  _darf_journal_lesen
 21802-21825  _db_maintenance_loop
  6359-6387   _db_vacuum_loop
 15254-15278  _detect_foreign_ad
  1442-1453   _diag_path_owner
 16674-16718  _director_finalize
 17485-17492  _director_for
 16623-16671  _director_mark
 22799-22834  _disc_automod_check
 22775-22778  _disc_state_get
 22781-22788  _disc_state_set
 19975-19979  _discord_invite
 22736-22772  _discord_live_thread
 16825-16837  _discord_notify
 19874-19899  _discord_ops_alert
 22634-22732  _discord_post_user
 20035-21764  _discord_run_once
 19914-19972  _discord_start
 22295-22301  _discord_stop
  6418-6495   _disk_alarm_loop
 24847-24896  _disk_autoclean
 24899-24912  _disk_guard_loop
 13010-13012  _drawtext_chain
 11714-11716  _dump_all_threads
 10399-10462  _enrich_proxies_with_geo
  2037-2081   _ensure_cookie_file_netscape
 19982-20032  _ensure_discord_invite
 22501-22533  _ensure_error_channel
  8235-8238   _ensure_notify_topic
 10643-10680  _ensure_proxy_ready
  8189-8216   _ensure_topic
   686-688    _env_int
   691-693    _env_int_range
 22601-22631  _error_channel_loop
 16870-16883  _event_webhook
 12390-12403  _evolution_loop
  5539-5573   _extract_file_payload
  2153-2155   _extract_urls_from_streamurl_node
 19193-19200  _f2b_sudo_hint
  4419-4429   _fehler_text
 10300-10318  _fetch_proxy_list
 17319-17347  _fetch_tiktok_room_id
   747-750    _ff_cmd
 13176-13181  _find_chromium
  3125-3129   _find_external_recorder
  2158-2160   _find_stream_urls
 12087-12112  _fire_webhooks
  7280-7289   _fork_safe
   847-860    _freeai_chat_sync_metered
 19239-19243  _geo_lookup_ips
  3583-3592   _get_ai_session
  7113-7153   _get_live_info
  2695-2702   _get_resolve_semaphore
  7513-7890   _handle_single_tracking
 24669-24671  _hb
 24674-24691  _hb_while
 12631-12633  _highlight_cfg
 12636-12665  _highlight_observe
 13184-13202  _htmlov_screenshot_cmd
 17063-17073  _httpx_proxy
 12120-12132  _in_quiet_hours
 25738-25769  _install_fast_eventloop
  9585-9639   _install_fast_json
 11719-11735  _install_faulthandler
 17978-17987  _intel_ensure_schema
 18025-18060  _intel_index_loop
 17999-18009  _intel_index_one
 17990-17996  _intel_semantic
  4908-4917   _is_authorized
  7414-7420   _is_dead
  2143-2145   _is_hevc
 19228-19230  _is_private_ip
  1606-1613   _is_process_running
  6127-6138   _is_quiet_hours
  1243-1252   _is_upload_window
  9674-9687   _json_error_handler
  6353-6354   _kick_broadcaster_id
  6265-6307   _kick_follower_count
  6249-6252   _kick_slug
 11233-11264  _kick_user_token
  3957-3960   _kind_from_filename
 12149-12154  _latest_popularity
 17700-17733  _live_react_loop
 17496-17689  _live_react_worker
 16279-16290  _live_transcript_push
 17691-17698  _live_users
 16721-16765  _living_title_loop
 21968-22040  _local_backup_scan
  9656-9670   _log_5xx
 13612-13624  _looks_like_codec_err
 13607-13609  _looks_like_source_expired
  7330-7360   _loop_fehler
 11739-11748  _loop_heartbeat
 24639-24666  _loop_lag_monitor
 11751-11819  _loop_watchdog_thread
 16159-16173  _loyalty_add
 16150-16156  _loyalty_get
 16176-16184  _loyalty_top
 12262-12264  _manual_donations_total
  4626-4645   _manual_status
  7422-7423   _mark_dead
 10919-10935  _marketing_loop
 23318-23336  _maybe_handle_command
 24998-25022  _maybe_hype_clip
  3875-3898   _migrate_columns
 23597-23608  _mod_is_exempt
 23611-23616  _mod_warn_first
 23619-23622  _mod_warn_text
 12430-12438  _modlog
   990-992    _multistream_targets
  7292-7293   _nc_create_subprocess_exec
  7296-7297   _nc_create_subprocess_shell
 11170-11187  _news_loop
 12457-12459  _normalize_ingest
  2336-2353   _note_check_duration
  8229-8232   _notify_topic_name
 16305-16313  _oracle_memories
 16578-16612  _oracle_memorize
 16316-16329  _oracle_persona
 16298-16302  _oracle_recent_text
 12791-12799  _ov_atomic_write
 12779-12785  _ov_bar
 15157-15169  _ov_clip_text
 12788-12789  _ov_oneline
 18905-18934  _overlay_push
 13130-13173  _overlay_render_size
 12523-12527  _overlay_session_reset
 18869-18872  _overlay_src_ok
 15241-15251  _own_invites
 13125-13127  _parse_size
 19414-19494  _parse_ssh_attacks
  6715-6748   _pause_resume_cmd
  1846-1890   _persist_refreshed_cookies
  1751-1783   _pick_checked_pull_proxy
  9755-9768   _pin_auth_value
  9814-9815   _pin_clear_fail
  9794-9797   _pin_locked
  9800-9811   _pin_note_fail
  9771-9791   _pin_ok
 18763-18788  _piper_pick_model
 18800-18847  _piper_say
 12049-12084  _post_json_threaded
 13104-13122  _probe_video_size
  1634-1651   _proc_is_recorder
 10612-10640  _proxy_pool_refresh_loop
  1717-1748   _proxy_report_recording
 11704-11706  _prune_stall_dumps
 10989-11110  _public_stats
 16841-16867  _push_notify
  9916-9918   _pwa_dir
 10369-10384  _quick_validate_proxy
 12115-12117  _quiet_hours_config
  9881-9914   _rate_guard
 16124-16130  _react_warn
  7200-7239   _reap_proc
  2376-2398   _record_check_outcome
   742-744    _redact_stream_urls
 10539-10609  _refresh_proxy_pool
  2169-2259   _resolve_via_html
  2518-2672   _resolve_via_webcast_api_v2
  2735-2797   _resolve_via_ytdlp
 22945-23074  _resolve_youtube_ingest
 12506-12517  _restream_active_sources
 17350-17449  _restream_chat_guardian
 12668-12740  _restream_chat_push
 12765-12774  _restream_chat_push_async
 13205-13292  _restream_html_overlay_start
 13295-13308  _restream_html_overlay_stop
 12468-12491  _restream_overlay_files
 17737-17769  _restream_platform_state
 17894-17929  _restream_resume_after_restart
 13356-13414  _restream_tts_enqueue_wav
 13066-13098  _restream_tts_feeder
 13063-13064  _restream_tts_fifo_path
 13311-13338  _restream_tts_start
 13340-13354  _restream_tts_stop
 17775-17891  _restream_verify_loop
 21933-21945  _retention_loop
 21927-21930  _retention_scan
  2480-2482   _room_is_abo
  5577-5694   _run_ai_call
 11842-11855  _run_async_from_flask
 19233-19236  _run_priv
 25726-25734  _run_selfcheck_and_exit
 21948-21959  _s3_client
  7449-7500   _safe_send
  4552-4568   _sample_net_throughput
  2428-2455   _schedule_next_check
 21881-21924  _scheduler_loop
  3901-3905   _schema_pk
 11859-11864  _scraper_session
 23625-23664  _screen_full
 11308-11345  _sec_headers
  2148-2150   _select_stream_from_data_section
 25539-25723  _selfcheck
  8241-8275   _send_live_notice
  1266-1270   _should_defer_upload
 22367-22402  _shrink_for_discord
  9921-9933   _sicheres_ziel
 21779-21799  _sicherheits_erinnerung_loop
 24919-24936  _sign_health_check
 24939-24958  _sign_health_loop
  7309-7320   _spawn
 26083-26113  _spawn_from_flask
 19515-19518  _st_befund
 17075-17316  _start_chat_listener
 11822-11839  _start_loop_watchdog
 11137-11165  _stats_loop
 11116-11119  _stats_output_path
 11122-11134  _stats_write
  7969-7985   _storage_cleanup_loop
 24978-24985  _story_for
  3187-3193   _stream_url_expiry
  3202-3208   _stream_url_is_fresh
  3195-3200   _stream_url_ttl
 15204-15211  _streamer_persona_get
 13015-13019  _studio_chain
 22065-22187  _system_backup
 22196-22226  _system_backup_loop
 10321-10360  _test_proxy
 10867-10883  _testpush_resolve_live
  7425-7446   _tg_sprache_setzen
  8148-8158   _tg_topics_load_into_mem
  8145-8146   _tg_topics_path
  8160-8167   _tg_topics_save
  9729-9737   _token_ok
  8170-8174   _topic_forget
 12135-12146  _tracking_max_duration
  4165-4179   _tracking_remove_cleanup
  4196-4208   _tracking_resume_cleanup
  1500-1523   _try_attach_file_handler
 18790-18798  _tts_cleanup
 10843-10847  _tunnel_effective
 18286-18339  _twitch_channel_status
 23667-23812  _twitch_chat_loop
 23481-23584  _twitch_eventsub_loop
  1289-1302   _upload_queue_add
  1313-1315   _upload_queue_count
  1272-1281   _upload_queue_load
  1262-1264   _upload_queue_path
  1304-1311   _upload_queue_remove
  1283-1287   _upload_queue_save
  1317-1358   _upload_window_loop
  7173-7180   _uptime_s
 12445-12454  _url_host
   807-811    _usage_record_claude
  7363-7407   _verbindung_verloren
  6310-6341   _viewer_sample_loop
  9818-9821   _wants_html
  7183-7197   _warn_empty_env
 24712-24833  _watchdog_loop
 23220-23228  _wchat_thank_ok
 16909-16939  _whisper_get_model
  7270-7277   _whisper_native_section
 16111-16117  _whisper_pool
 17008-17037  _whisper_segments
 16941-17005  _whisper_transcribe
 12846-13008  _write_restream_overlay
 12808-12843  _write_restream_overlay_async
 23836-23916  _youtube_api_chat_loop
 18342-18445  _youtube_api_status
 18448-18515  _youtube_channel_status
 23919-24080  _youtube_chat_loop
 23080-23093  _youtube_restream_autoconfig
 23096-23120  _youtube_restream_autoconfig_inner
 23187-23215  _youtube_send
 18583-18624  _youtube_set_channel
 23123-23157  _yt_access_token
 23160-23175  _yt_live_chat_id
 23183-23184  _yt_sendrate_cfg
 23815-23830  _yt_timeout
  2719-2720   _ytdlp_detect_available
  2722-2733   _ytdlp_note_result
 11709-11711  _zombie_child_count
  7049-7073   about
  4076-4080   add_ai_log_entry
  3993-3996   add_archive_entry
  4590-4592   add_archive_rule
  4367-4401   add_recording
  4140-4157   add_tracking
  5697-5730   ai
  3728-3779   ai_chat
  3813-3823   ai_history_append
  3825-3830   ai_history_clear
  3802-3811   ai_history_load
  3787-3800   ai_rate_limit_check
  5759-5767   aireset
 16446-16465  azrael_chat
 24085-24207  brain_cmd
  3211-3395   build_recording_cmd
  4160-4163   bulk_add_trackings
  6546-6605   bulkadd
  7988-8128   check_all_trackings
  4212-4224   claim_live_transition
 15281-16043  class KickModerator
 13627-15044  class RestreamManager
 10726-10768  classify_proxy_anonymity
  5805-6003   cleanup
  4844-4850   cleanup_old_recordings
  4358-4365   clear_recording
 22837-22902  clip_moment
  4542-4545   compute_storage_forecast
  6668-6712   cookies_cmd
  4131-4137   count_trackings_for_chat
  4063-4074   decide_preferred_recorder
  4003-4006   delete_archive_entry
  4594-4596   delete_archive_rule
  5234-5381   diag
 24319-24380  einnahmen_cmd
  4536-4539   find_recordings_by_fingerprint
  4024-4040   finish_recording_attempt
  4184-4186   get_all_active_trackings
  4091-4093   get_all_checks
  4403-4406   get_all_recordings
  4485-4487   get_all_tags_with_counts
  4513-4516   get_annotations_for_recording
  3998-4001   get_archive_entry
  4506-4509   get_bookmarked_recordings
  1913-2030   get_cookie_health
  4473-4479   get_event_log
  4047-4061   get_last_recording_attempt
  2800-2905   get_live_status
  4783-4786   get_manual_recordings
  4521-4524   get_or_compute_inspect_sync
  4885-4888   get_outcome_breakdown
  4492-4495   get_priority_poll_interval
  4042-4045   get_recent_recording_attempts
  4408-4411   get_recording_by_id
  4499-4502   get_recording_note
  3529-3552   get_redis
  4120-4123   get_stats
  4838-4842   get_storage_stats
  4614-4616   get_tiktok_status_distribution
  4226-4235   get_tracking_state
  4181-4182   get_trackings_for_group
  4799-4802   get_trash_recordings
  8896-9564   handle_recording_finished
  3923-3948   init_db
  4586-4588   list_archive_rules
  5038-5076   live
  7503-7511   live_check_worker
  3607-3641   llm_chat
  3664-3692   llm_chat_sync
  3649-3661   llm_list_models
  4432-4465   log_event
  1568-1601   log_recording_failure
  6862-6911   logs_cmd
 25026-25529  main
  5733-5756   on_ai_media
  6988-7014   on_ai_reply
  7017-7046   on_azrael_mention
  7078-7108   on_callback
 16471-16575  oracle_handle
  6751-6754   pause_tracking
  4898-4903   profile_keyboard
  6813-6859   quota
  7892-7966   reaper_loop
  4610-4612   record_tiktok_status
  5772-5802   recstatus
  3554-3562   redis_get_json
  3565-3571   redis_set_json
 24383-24393  report_cmd
 10771-10773  report_proxy_result
  2262-2289   resolve_tiktok_live_stream
  4794-4797   restore_recording
  6757-6760   resume_tracking
  4599-4604   run_archive_rules
 24396-24619  run_bot
 11624-11676  run_flask
  4574-4577   sample_bandwidth_for_active
  4083-4089   save_tiktok_check
  4350-4356   set_recording_file
  4189-4193   set_tracking_paused
  4789-4792   soft_delete_recording
  8281-8894   split_and_send_video
  4951-4993   start
  4008-4022   start_recording_attempt
  6006-6044   stats
  4764-4781   stop_manual_recording
  6763-6810   stoprec
  6234-6242   summary_cmd
  6914-6985   sysres
  5383-5527   teststream
  4995-5036   tiktok
  6608-6665   topusers
  5113-5170   track
  5078-5110   track_exact
  5184-5232   tracklist
  4648-4762   trigger_manual_recording
  4311-4348   try_acquire_recording_lock
  4805-4807   universal_search
  5172-5182   untrack
 24210-24316  update_cmd
  4531-4534   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             configure, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            geschuetzt, host, lage, nur_lokal, offen_im_netz
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls, url_ohne_zugang
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
whispercfg.py          geladen, name, verfuegbar, waehle
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
